"""
kor_yt_md_pipeline.py

한국어 강의 유튜브 영상 → 구조화된 .md 변환 파이프라인 (Korean 트랙 전용).
규칙서: _vault_setup\01_md_convert\korean_yt_md_guide.md

[핵심 설계]
돈 드는 일(영상 100시간 보고 듣기)은 전부 로컬(RTX 4070)에서 무료로 처리하고,
Gemini 3 Flash에는 "타임라인 텍스트 + distinct 프레임 이미지"만 보내 .md만 쓰게 한다.
영상 자체를 클라우드에 안 보내므로 비용이 예측 가능하고 Rate Limit 위험이 작다.

[입력]
01_Raw/00_Curriculum_and_index/02_yt_md_convert.xlsx 를 직접 파싱한다 (커리큘럼맵 .md 파싱 방식 폐기).
md보유여부 컬럼: X=미변환(대상) / O=변환완료 / F=검증실패(사람 검토 대기). X인 행만 처리한다.
출력 폴더는 title 재구성이 아니라 01_Raw/01_by_level_lesson/Level_{n}/{lesson_num}_* 글롭 매칭으로 찾는다
(이미 존재하는 레슨 폴더만 사용 — 없으면 자동 생성하지 않고 실패 처리).

[영상 1개 처리 8단계]
  1. 중복확인  : 이미 .md 있으면 건너뛰고 복제 폴더에 복사만 (xlsx 상태도 O로 갱신)
  2. 다운로드  : 480p mp4 1개만 (yt-dlp)
  3. 분리      : ffmpeg로 오디오(16k mono) + 분석용 프레임 추출
  4. 받아쓰기  : faster-whisper large-v3 + VAD (무음 구간 환각 차단)
  5. 키프레임  : 화면 변화 감지로 distinct 프레임만 보존(지각해시 dedup) → OCR
  6. 타임라인  : AUDIO 트랙 + SCREEN(OCR) 트랙을 시간순으로 병합
  7. 합성      : Gemini 3 Flash에 (타임라인 + 프레임 이미지 + OCR 앵커) → .md
  8. 검증/저장 : 규칙·커버리지 검사 → 실패 시 1회 재생성 →
                성공: 저장 + xlsx X→O / 실패: 04_convert_fail/ 보관(삭제 안 함) + xlsx X→F

[사용법]
    python kor_yt_md_pipeline.py --dry-run        # 작업 목록만 (API 호출 없음)
    python kor_yt_md_pipeline.py --limit 2        # 시범 2개
    python kor_yt_md_pipeline.py --level 1        # 특정 레벨만
    python kor_yt_md_pipeline.py                  # 전체(X 상태) 일괄
    python kor_yt_md_pipeline.py --turbo          # Whisper large-v3-turbo (속도 우선)

[설치]
    pip install google-genai yt-dlp faster-whisper paddleocr pillow python-dotenv openpyxl
    ffmpeg는 PATH에 있어야 함. CUDA GPU 권장.
    .env 에 GEMINI_API_KEY 필요 (선택: YTDLP_COOKIES_FILE).
"""

import argparse
import asyncio
import json
import logging
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path

import openpyxl

# 윈도우 콘솔에서 한글 깨짐 방지
if hasattr(sys.stdout, "reconfigure") and sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure") and sys.stderr.encoding != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# pip으로 설치된 nvidia CUDA DLL(cublas64_12.dll 등)을 ctranslate2가 찾을 수 있도록
# site-packages/nvidia/*/bin 경로를 PATH와 DLL 검색 경로에 추가
def _register_nvidia_dlls() -> None:
    try:
        import site
        for sp in site.getsitepackages():
            nvidia_root = Path(sp) / "nvidia"
            if not nvidia_root.is_dir():
                continue
            for pkg_dir in nvidia_root.iterdir():
                bin_dir = pkg_dir / "bin"
                if bin_dir.is_dir():
                    bin_str = str(bin_dir)
                    if bin_str not in os.environ.get("PATH", ""):
                        os.environ["PATH"] = bin_str + os.pathsep + os.environ.get("PATH", "")
                    if hasattr(os, "add_dll_directory"):
                        try:
                            os.add_dll_directory(bin_str)
                        except OSError:
                            pass
    except Exception:
        pass

_register_nvidia_dlls()


# ─────────────────────────── 경로 / 상수 ────────────────────────────
# 핵심: 경로를 하드코딩하지 않는다. (v1의 가장 큰 버그)
# 이 스크립트가 놓인 폴더를 프로젝트 루트로 자동 인식. .env의 BASE_DIR로 덮어쓰기 가능.

def _detect_base_dir() -> Path:
    env = os.environ.get("BASE_DIR", "").strip()
    if env:
        return Path(env)
    # 이 스크립트 위치: <vault>\_vault_setup\01_md_convert\_scripts\
    # 따라서 vault 루트는 세 단계 위(parents[3]).
    return Path(__file__).resolve().parents[3]


BASE_DIR        = _detect_base_dir()
SCRIPT_DIR      = Path(__file__).resolve().parent
RAW_LESSON_BASE = BASE_DIR / "01_Raw" / "01_by_level_lesson"
XLSX_PATH       = BASE_DIR / "01_Raw" / "00_Curriculum_and_index" / "02_yt_md_convert.xlsx"
EXEMPLARY_MD    = (
    RAW_LESSON_BASE / "Level_1" / "4_Yes_No" / "02_yt_md"
    / "Your Korean Saem_A Full Korean Conversation Just With 네!.md"
)
GEN_DIR        = SCRIPT_DIR / "claude_gen"        # 로그·실패기록·manifest (숨김 폴더 아님)
FAIL_LOG       = GEN_DIR / "변환_실패_log.md"
PROC_LOG       = GEN_DIR / "pipeline_log.txt"
MANIFEST       = GEN_DIR / "manifest.json"         # 완료 URL·비용 기록 (재개용)
ACTIVE_JOBS    = GEN_DIR / "active_jobs.json"      # 현재 처리 중인 영상 목록 (모니터용)
FAILED_MD_DIR  = SCRIPT_DIR.parent / "result_check" / "convert_F"
# 검증 실패 .md 보관. 삭제 금지 — 사람이 검토.
# 2026-08-31 Ji 요청으로 04_convert_fail → 01_inbox\result_check\convert_F로 이동.
# 2026-09-03 Ji가 result_check를 01_inbox에서 _vault_setup\01_md_convert로 이동.
# (성공 저장 경로 RAW_LESSON_BASE는 그대로 둠 — 01_inbox 평면 출력 전환은 별도 미완 작업)

# ── 모델 / 합성 설정 ──
MODEL_NAME      = os.environ.get("GEMINI_MODEL", "gemini-3-flash-preview")
GEMINI_TEMP     = 0.2  # 더 낮춤: 더 deterministic하고 신중한 출력 유도
THINKING_BUDGET = int(os.environ.get("GEMINI_THINKING", "2048"))  # 상향: 복잡한 작업에 더 신중함

# ── 프레임(시각 캡처) 설정 ──
INTERNAL_FPS    = 2.0     # 변화 감지용 내부 샘플링 (초당 N장). 화면≥0.5초면 포착
PHASH_THRESHOLD = 6       # 평균해시 해밍거리 <= 이 값이면 "같은 화면"으로 보고 합침
MAX_FRAMES      = 60      # 영상당 Gemini로 보낼 최대 프레임(비용 상한)
JPEG_QUALITY    = 3       # ffmpeg -q:v (낮을수록 고화질)

# ── 동시성 설정 ──
PIPELINE_CONC   = 10      # 동시에 진행하는 영상 수 (자원별 세마포어가 실제 병목 제어)
DL_CONC         = 4       # 동시 다운로드
GPU_CONC        = 1       # Whisper는 GPU 1슬롯 직렬
GEMINI_CONC     = 1       # Gemini 동시 호출 (8은 이 키의 RPM/TPM 쿼터를 초과해 429 연쇄 발생 → 1로 축소)
GEMINI_MIN_INTERVAL_SEC = float(os.environ.get("GEMINI_MIN_INTERVAL_SEC", "20"))  # 호출 시작 최소 간격

# ── 비용 설정 (Gemini 3 Flash Standard, 백만 토큰당 USD) ──
PRICE_IN        = 0.50    # 입력(text/image/video)
PRICE_CACHED_IN = 0.05    # 캐시된 입력
PRICE_OUT       = 3.00    # 출력(thinking 포함)
KRW_PER_USD     = float(os.environ.get("KRW_PER_USD", "1350"))
BUDGET_KRW      = float(os.environ.get("BUDGET_KRW", "999999999"))  # 지출 한도는 Google AI Studio에서 관리

# 레벨 키 → 01_by_level_lesson 하위 최상위 폴더명.
# 숫자 레벨(1~12 등)은 get_target_folder()에서 f"Level_{level}"로 폴백 처리하므로 여기 없어도 됨.
LEVEL_TOP_MAP = {
    "VSL":     "00_VSL",
    "Intro":   "01_Intro",
    "Hangul":  "02_Hangul",
    "Numbers": "03_Numbers",
}

# Whisper 받아쓰기 유도 프롬프트 (한국어 단어는 한글로)
_WHISPER_PROMPT = (
    "This is a Korean language teaching video. The instructor speaks primarily in English "
    "but frequently uses Korean words and example sentences written in Hangul. "
    "Korean words must be transcribed in Hangul (한글), not romanized. "
    "English must remain in English. Do not translate either language."
)


class BudgetExceeded(Exception):
    """누적 비용이 한도(₩20,000)에 도달하면 발생 → 전체 정지."""


# ─────────────────────────────── 로깅 ──────────────────────────────────

def setup_logging() -> None:
    GEN_DIR.mkdir(parents=True, exist_ok=True)
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    if root.handlers:
        return
    fh = logging.FileHandler(str(PROC_LOG), encoding="utf-8", mode="a")
    fh.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    root.addHandler(fh)
    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    root.addHandler(ch)


# ─────────────────────────── 비용 추적기 ───────────────────────────────

class CostTracker:
    """Gemini usage_metadata를 누적해 USD/원화 환산. 한도 초과 여부 판단."""

    def __init__(self, budget_krw: float):
        self.budget_krw = budget_krw
        self.in_tokens = 0
        self.cached_tokens = 0
        self.out_tokens = 0
        self.usd = 0.0
        self._lock = asyncio.Lock()

    async def add(self, usage) -> None:
        # usage_metadata 필드를 방어적으로 읽음 (SDK 버전별 명칭 차이 대비)
        prompt = getattr(usage, "prompt_token_count", 0) or 0
        cached = getattr(usage, "cached_content_token_count", 0) or 0
        cand   = getattr(usage, "candidates_token_count", 0) or 0
        think  = getattr(usage, "thoughts_token_count", 0) or 0
        non_cached_in = max(prompt - cached, 0)
        cost = (
            non_cached_in * PRICE_IN
            + cached * PRICE_CACHED_IN
            + (cand + think) * PRICE_OUT
        ) / 1_000_000
        async with self._lock:
            self.in_tokens += non_cached_in
            self.cached_tokens += cached
            self.out_tokens += cand + think
            self.usd += cost

    @property
    def krw(self) -> float:
        return self.usd * KRW_PER_USD

    def over_budget(self) -> bool:
        return self.krw >= self.budget_krw

    def summary(self) -> str:
        return (
            f"누적 비용 ${self.usd:.3f} (≈₩{self.krw:,.0f}) / 한도 ₩{self.budget_krw:,.0f} | "
            f"입력 {self.in_tokens:,} (캐시 {self.cached_tokens:,}) · 출력 {self.out_tokens:,} 토큰"
        )


# ──────────────────────── 워커 / 모델 상태 ─────────────────────────────

class PipelineWorkers:
    """무거운 모델은 지연 로딩. 자원별 세마포어 보유."""

    def __init__(self) -> None:
        self.gemini_client = None
        self._whisper = None
        self._ocr = None
        self.whisper_name = "large-v3"
        self.gpu_sem    = asyncio.Semaphore(GPU_CONC)
        self.dl_sem     = asyncio.Semaphore(DL_CONC)
        self.gemini_sem = asyncio.Semaphore(GEMINI_CONC)
        self._gemini_pace_lock = asyncio.Lock()
        self._gemini_last_call = 0.0

    async def throttle_gemini(self) -> None:
        """호출 시작 간 최소 간격을 강제 → 429(RPM/TPM 초과) 연쇄 방지."""
        async with self._gemini_pace_lock:
            now = time.monotonic()
            wait = self._gemini_last_call + GEMINI_MIN_INTERVAL_SEC - now
            if wait > 0:
                await asyncio.sleep(wait)
            self._gemini_last_call = time.monotonic()

    def init_gemini(self, api_key: str) -> None:
        from google import genai  # 지연 import
        self.gemini_client = genai.Client(api_key=api_key)

    def get_whisper(self):
        if self._whisper is None:
            from faster_whisper import WhisperModel
            try:
                logging.info(f"faster-whisper {self.whisper_name} CUDA 로딩...")
                self._whisper = WhisperModel(self.whisper_name, device="cuda", compute_type="float16")
            except Exception as e:
                logging.warning(f"CUDA 불가({e}) → CPU 폴백")
                self._whisper = WhisperModel(self.whisper_name, device="cpu", compute_type="int8")
        return self._whisper

    def get_ocr(self):
        if self._ocr is None:
            from paddleocr import PaddleOCR
            logging.info("PaddleOCR(korean, CPU) 로딩...")
            # OCR은 CPU로 (GPU는 Whisper 전용 → 8GB VRAM 경합 방지)
            # PaddleOCR 3.x는 show_log/use_gpu 인자를 제거했음 → 단순 호출로 폴백
            for kwargs in [
                {"lang": "korean", "use_gpu": False, "show_log": False},
                {"lang": "korean", "use_gpu": False},
                {"lang": "korean"},
            ]:
                try:
                    self._ocr = PaddleOCR(**kwargs)
                    break
                except (TypeError, ValueError):
                    continue
            if self._ocr is None:
                raise RuntimeError("PaddleOCR 초기화 실패: 지원되는 인자 조합 없음")
        return self._ocr


# ──────────────────────── xlsx 파서 (02_yt_md_convert.xlsx) ────────────
# 컬럼(0-base): 0 Ji레벨 / 1 Ji레슨 / 2 Ji레슨Title / 3 Raw종류 / 4 채널 / 5 Playlist /
#              6 Ref_No / 7 영상타이틀 / 8 링크 / 9 md보유여부(X/O/F) / 10 추가변환필요여부

def _cell_str(v) -> str:
    if v is None:
        return ""
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    return str(v).strip()


def parse_xlsx() -> list:
    """02_yt_md_convert.xlsx 전체 행을 파싱. status(X/O/F)와 원본 엑셀 row 번호를 포함해 반환."""
    wb = openpyxl.load_workbook(XLSX_PATH, data_only=True)
    ws = wb[wb.sheetnames[0]]
    entries = []
    for row_idx, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
        if not row:
            continue
        row = list(row) + [None] * (11 - len(row))
        level, lesson_num, lesson_title, _raw_type, channel, playlist, _ref_no, \
            video_title, url, status, _need = row[:11]
        url = _cell_str(url)
        if not url or not is_youtube_url(url):
            continue
        level_s = _cell_str(level)
        try:
            n = int(float(lesson_num))
            lesson_id = f"{level_s}-{n:02d}"
        except (ValueError, TypeError):
            n = _cell_str(lesson_num)
            lesson_id = f"{level_s}-{n}"
        entries.append({
            "level": level_s, "lesson_num": n,
            "lesson_title": _cell_str(lesson_title), "lesson_id": lesson_id,
            "channel": _cell_str(channel), "playlist": _cell_str(playlist),
            "video_title": _cell_str(video_title), "url": url,
            "status": _cell_str(status).upper(), "row": row_idx,
        })
    wb.close()
    return entries


# ── xlsx md보유여부 컬럼 자동 갱신 (X→O 완료 / X→F 검증실패) ──
XLSX_STATUS_COL = 10   # J열: md보유여부
_xlsx_save_lock = asyncio.Lock()


def _update_xlsx_status_sync(row: int, status: str) -> None:
    try:
        wb = openpyxl.load_workbook(XLSX_PATH)
        ws = wb[wb.sheetnames[0]]
        ws.cell(row=row, column=XLSX_STATUS_COL).value = status
        wb.save(XLSX_PATH)
        wb.close()
    except Exception as exc:
        # xlsx가 Excel에서 열려있는 등으로 저장 실패해도 파이프라인은 계속 진행 (manifest가 진행상황을 별도 보존)
        logging.warning(f"xlsx 상태 갱신 실패(row={row} → {status}): {exc}")


async def update_xlsx_status(row: int, status: str) -> None:
    loop = asyncio.get_event_loop()
    async with _xlsx_save_lock:
        await loop.run_in_executor(None, _update_xlsx_status_sync, row, status)


async def update_xlsx_status_many(rows: list, status: str) -> None:
    for r in rows:
        await update_xlsx_status(r, status)


# ──────────────────── 폴더 / 파일명 헬퍼 ────────────────────────────────

def get_target_folder(entry: dict) -> Path:
    """레벨·레슨 번호로 이미 존재하는 01_by_level_lesson 폴더를 글롭 매칭해서 찾는다.
    title로부터 폴더명을 재구성하지 않는다 — Raw 폴더 구조는 이미 고정돼 있으므로
    해당 레벨/레슨 폴더가 없으면 자동 생성하지 않고 예외를 던진다."""
    top_name = LEVEL_TOP_MAP.get(entry["level"], f"Level_{entry['level']}")
    top_folder = RAW_LESSON_BASE / top_name
    if not top_folder.exists():
        raise FileNotFoundError(f"레벨 폴더 없음: {top_folder}")
    prefix = f"{entry['lesson_num']}_"
    matches = sorted(p for p in top_folder.iterdir() if p.is_dir() and p.name.startswith(prefix))
    if not matches:
        raise FileNotFoundError(f"레슨 폴더 없음: {top_folder}\\{prefix}*")
    return matches[0] / "02_yt_md"


def make_filename(channel: str, playlist: str, video_title: str) -> str:
    parts = [channel]
    if playlist:
        parts.append(playlist)
    parts.append(video_title)
    name = "_".join(parts) + ".md"
    return re.sub(r'[<>:"/\\|?*\n\r]', "", name).strip()


def is_youtube_url(url: str) -> bool:
    if "youtube.com/playlist" in url or "youtube.com/channel" in url:
        return False
    return "youtube.com" in url or "youtu.be" in url


def build_work_list(primary_entries: list, all_entries: list):
    """
    primary_entries: 필터된 목록(md보유여부=X, --level 등 적용됨) — 이번 실행에서 변환할 영상 결정
    all_entries: xlsx 전체 행 — secondary_map(복사 대상 폴더) 구성에 사용
    동일 URL은 1회만 변환(primary), 나머지 레슨 폴더는 전부 복사 대상(secondary).
    실행 범위(--level 등)와 무관하게 xlsx 전체 기준으로 복사 목록을 만든다.
    secondary 항목은 (folder, filename, entry) — entry는 복사 후 해당 xlsx row를 O로 갱신하는 데 쓰임.
    """
    all_dests: dict = {}
    for entry in all_entries:
        url = entry["url"]
        try:
            folder = get_target_folder(entry)
        except FileNotFoundError as e:
            logging.warning(f"복사 대상 폴더 확인 불가(건너뜀): {e}")
            continue
        filename = make_filename(entry["channel"], entry["playlist"], entry["video_title"])
        all_dests.setdefault(url, []).append((folder, filename, entry))

    seen = {}
    secondary_map = {}
    primary_list = []
    for entry in primary_entries:
        url = entry["url"]
        if url in seen:
            continue
        seen[url] = True
        try:
            folder = get_target_folder(entry)
        except FileNotFoundError as e:
            logging.error(f"레슨 폴더 없음 → 이번 실행에서 건너뜀: {e}")
            continue
        filename = make_filename(entry["channel"], entry["playlist"], entry["video_title"])
        primary_list.append((entry, folder, filename))
        # 전체 xlsx에서 이 URL의 모든 레슨 폴더 중 primary 제외한 나머지가 복사 대상
        secondary_map[url] = [
            (f, n, e) for f, n, e in all_dests.get(url, [])
            if not (f == folder and n == filename)
        ]
    return primary_list, secondary_map


# ───────────────────────── yt-dlp / ffmpeg ────────────────────────────

def _ytdlp_base() -> list:
    # "yt-dlp" 콘솔스크립트 exe 래퍼가 이 환경에서 깨져있어(rc=1, 무출력) 항상 조용히 실패함.
    # venv 파이썬으로 yt_dlp 모듈을 직접 실행하면 정상 동작하므로 이 경로를 사용.
    cmd = [sys.executable, "-m", "yt_dlp", "--js-runtimes", "node"]
    cookies_file = os.environ.get("YTDLP_COOKIES_FILE", "")
    if cookies_file:
        p = Path(cookies_file)
        if not p.is_absolute():
            p = BASE_DIR / cookies_file
        cmd += ["--cookies", str(p)]
    else:
        browser = os.environ.get("YTDLP_COOKIES_BROWSER", "")
        if browser:
            cmd += ["--cookies-from-browser", browser]
    return cmd


async def _run(args: list) -> tuple:
    proc = await asyncio.create_subprocess_exec(
        *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    out, err = await proc.communicate()
    return proc.returncode, out.decode("utf-8", "replace"), err.decode("utf-8", "replace")


async def fetch_metadata(url: str) -> dict:
    rc, out, err = await _run(_ytdlp_base() + ["--dump-json", "--no-playlist", url])
    if rc != 0 or not out.strip():
        raise RuntimeError(f"yt-dlp 메타데이터 실패: {err[:300]}")
    return json.loads(out)


async def download_video(url: str, video_dir: Path, dl_sem) -> Path:
    """480p mp4 1개만 다운로드 (오디오·프레임은 로컬에서 이 파일로 뽑음)."""
    video_dir.mkdir(parents=True, exist_ok=True)
    out_tmpl = str(video_dir / "video.%(ext)s")
    cmd = _ytdlp_base() + [
        "-f", "bestvideo[height<=480]+bestaudio/best[height<=480]",
        "--merge-output-format", "mp4", "--no-playlist", "-o", out_tmpl, url,
    ]
    async with dl_sem:
        rc, _, err = await _run(cmd)
    if rc != 0:
        raise RuntimeError(f"yt-dlp 영상 다운로드 실패: {err[:300]}")
    cands = [p for p in video_dir.glob("video.*") if p.is_file()]
    if not cands:
        raise FileNotFoundError("다운로드된 영상 파일 없음")
    return cands[0]


def extract_audio_sync(video_path: Path, out_dir: Path) -> Path:
    """ffmpeg로 16k mono wav 추출 (Whisper 입력용)."""
    out = out_dir / "audio.wav"
    subprocess.run(
        ["ffmpeg", "-i", str(video_path), "-vn", "-ac", "1", "-ar", "16000", "-y", str(out)],
        capture_output=True, timeout=600,
    )
    if not out.exists():
        raise RuntimeError("ffmpeg 오디오 추출 실패")
    return out


def extract_frames_sync(video_path: Path, frames_dir: Path, fps: float) -> list:
    """ffmpeg로 fps 간격 프레임 추출. (path, ts초) 리스트 반환."""
    frames_dir.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["ffmpeg", "-i", str(video_path), "-vf", f"fps={fps}",
         "-q:v", str(JPEG_QUALITY), "-y", str(frames_dir / "f_%05d.jpg")],
        capture_output=True, timeout=1200,
    )
    files = sorted(frames_dir.glob("f_*.jpg"))
    frames = []
    for i, p in enumerate(files):
        ts = i / fps   # i번째(0-base) 프레임 시각
        frames.append((p, ts))
    return frames


# ──────────────────────── Whisper (VAD) ───────────────────────────────

def whisper_transcribe_sync(model, audio_path: str) -> list:
    """VAD 필터 ON → 무음 구간 환각 차단. (start, end, text) 리스트 반환."""
    segments, info = model.transcribe(
        audio_path,
        beam_size=5,
        task="transcribe",
        initial_prompt=_WHISPER_PROMPT,
        vad_filter=True,                                  # 핵심: 무음 환각 차단
        vad_parameters=dict(min_silence_duration_ms=500),
    )
    logging.info(f"Whisper 감지 언어: {info.language} (prob={info.language_probability:.2f})")
    out = []
    for seg in segments:
        t = seg.text.strip()
        if t:
            out.append((float(seg.start), float(seg.end), t))
    return out


# ──────────────────────── 키프레임 선별 (무손실) ──────────────────────

def _avg_hash(path: Path) -> int:
    """평균 해시(aHash): 8x8 흑백 축소 → 평균 기준 64비트. PIL만 사용."""
    from PIL import Image
    img = Image.open(path).convert("L").resize((8, 8))
    px = list(img.getdata())
    avg = sum(px) / len(px)
    bits = 0
    for i, v in enumerate(px):
        if v >= avg:
            bits |= (1 << i)
    return bits


def _hamming(a: int, b: int) -> int:
    return bin(a ^ b).count("1")


def select_keyframes_sync(frames: list, ocr) -> list:
    """
    화면 변화 감지로 distinct 프레임만 보존(무손실), 보존분만 OCR.
    반환: [(path, ts, ocr_text), ...]
    원리: 직전 보존 프레임 대비 (1)지각해시가 충분히 다르거나 (2)OCR 텍스트가 다르면 보존.
    """
    kept = []
    last_hash = None
    last_ocr = None
    for path, ts in frames:
        try:
            h = _avg_hash(path)
        except Exception:
            continue
        visual_changed = (last_hash is None) or (_hamming(h, last_hash) > PHASH_THRESHOLD)
        if not visual_changed:
            continue  # 화면 거의 동일 → 중복, 버림
        text = _run_ocr(ocr, str(path))
        # 시각도 비슷하고 글자도 같으면 진짜 중복 (애니메이션 미세변화 제외)
        if last_ocr is not None and text == last_ocr and not visual_changed:
            continue
        kept.append((path, ts, text))
        last_hash, last_ocr = h, text

    # 상한 초과 시: 변화량(직전 대비 해밍거리) 큰 순으로 솎되, 시간 순서는 유지
    if len(kept) > MAX_FRAMES:
        scored = []
        prev = None
        for idx, (p, ts, t) in enumerate(kept):
            try:
                hh = _avg_hash(p)
            except Exception:
                hh = 0
            score = 64 if prev is None else _hamming(hh, prev)
            score += min(len(t), 200) // 20   # OCR 텍스트 많은 프레임 가산점(정보량)
            scored.append((score, idx, (p, ts, t)))
            prev = hh
        top = sorted(scored, key=lambda x: -x[0])[:MAX_FRAMES]
        kept = [item for _, _, item in sorted(top, key=lambda x: x[1])]
    return kept


def _run_ocr(ocr, image_path: str) -> str:
    try:
        result = ocr.ocr(image_path, cls=True)
        if not result or not result[0]:
            return ""
        lines = []
        for item in result[0]:
            if isinstance(item, (list, tuple)) and len(item) >= 2:
                tc = item[1]
                lines.append(str(tc[0]) if isinstance(tc, (list, tuple)) else str(tc))
            elif hasattr(item, "text"):
                lines.append(item.text)
        return " ".join(lines).strip()
    except Exception as exc:
        logging.debug(f"OCR 오류 {image_path}: {exc}")
        return ""


# ──────────────────────── 타임라인 병합 ───────────────────────────────

def _mmss(sec: float) -> str:
    s = int(sec)
    return f"{s // 60:02d}:{s % 60:02d}"


def build_timeline(segments: list, keyframes: list) -> str:
    """
    AUDIO 트랙(Whisper)과 SCREEN 트랙(키프레임 OCR)을 시간순으로 병합.
    화면 상태 i는 [ts_i, ts_{i+1}) 구간 동안 떠 있다고 보고, 그 구간의 오디오를 묶는다.
    무음 구간은 (무음)으로 명시 → 화면 전용 콘텐츠가 절대 누락되지 않게 함.
    """
    if not keyframes:
        # 프레임이 없으면 오디오만 시간순으로
        return "\n".join(f"[{_mmss(s)}–{_mmss(e)}] AUDIO: \"{t}\"" for s, e, t in segments) or "(내용 없음)"

    # 화면 상태 경계
    bounds = [ts for _, ts, _ in keyframes] + [float("inf")]
    lines = []
    prev_screen = None
    for i, (_, ts, ocr_text) in enumerate(keyframes):
        win_start, win_end = bounds[i], bounds[i + 1]
        # 이 화면 구간에 중심점이 들어오는 오디오 세그먼트 모으기
        spoken = [t for (s, e, t) in segments if win_start <= (s + e) / 2 < win_end]
        audio_str = " ".join(spoken) if spoken else "(무음)"
        end_label = _mmss(win_end) if win_end != float("inf") else "끝"
        lines.append(f"[{_mmss(win_start)}–{end_label}] AUDIO: \"{audio_str}\"")
        # 화면 텍스트는 직전과 다를 때만 (중복 표기 방지)
        if ocr_text and ocr_text != prev_screen:
            lines.append(f"  SCREEN: \"{ocr_text}\"")
            prev_screen = ocr_text
        elif not ocr_text:
            lines.append("  SCREEN: (그래픽/비텍스트 화면 — 첨부 프레임 이미지 참조)")
    return "\n".join(lines)


def collect_korean_anchors(keyframes: list) -> list:
    """화면 OCR에서 한글 토큰 추출 → Whisper 철자 교정용 정답지 + 커버리지 검사용. 1글자 단어도 포함."""
    toks = set()
    for _, _, text in keyframes:
        # 1글자 이상 한글 단어 모두 포함 (기존: 2글자 이상만)
        for m in re.findall(r"[가-힣]+", text or ""):
            if m:  # 빈 문자 제외
                toks.add(m)
    return sorted(toks)


# ──────────────────────── 시스템 프롬프트 ─────────────────────────────

def build_system_prompt() -> str:
    """규칙 + exemplary 전문. 호출마다 동일 → 암묵 캐싱으로 입력비 절감."""
    exemplary = ""
    if EXEMPLARY_MD.exists():
        exemplary = EXEMPLARY_MD.read_text(encoding="utf-8")
    else:
        raise FileNotFoundError(
            f"Exemplary .md 필수: {EXEMPLARY_MD}\n"
            f"exemplary 파일 없으면 Gemini가 올바른 형식/상세도를 모르고 합성합니다."
        )

    return f"""You convert a Korean-language teaching YouTube video into a structured Markdown document.
This .md becomes raw source material for Korean lesson drafts. An LLM reading ONLY this file must be
able to faithfully reconstruct everything the video taught, including everything shown on screen.

═══ INPUT YOU RECEIVE ═══
- [VIDEO METADATA]
- [TIMELINE]: AUDIO track (Whisper) and SCREEN track (on-screen OCR) merged in time order.
  When AUDIO is "(무음)" the SCREEN text IS the teaching content for that moment.
- [KEY FRAMES]: the distinct on-screen states as images, in time order. LOOK at them directly.
- [OCR ANCHORS]: Korean words detected on screen = the correct spellings (ground truth).

═══ OUTPUT STRUCTURE ═══
# [Channel Name] | [Video Title]

## Metadata
(bullet list ONLY — table format "| Field | Content |" is STRICTLY FORBIDDEN)
- **Channel:** ...
- **Playlist:** ...        ← omit this line entirely if no playlist
- **URL:** ...
- **Duration:** [MM:SS]
- **Upload Date:** [YYYY-MM-DD]
- **Mapped Ji Lesson:** [lesson_id] [lesson_title]

---

## Teaching Points

### Overview
(2–3 paragraphs: the instructor's approach, framing, and learning arc)

---

### [Descriptive Section Title — NO number prefix]
(prose paragraphs)

---

## Transcript
(full verbatim speech, no timestamps)

═══ LANGUAGE RULES ═══
- All explanation/analysis in ENGLISH.
- Korean stays in Hangul AS-IS. NEVER romanize. ✓ "이다 means 'to be'"  ✗ "ida means 'to be'"
- Every Korean expression gets an English gloss: inline `먹다 (to eat)`, or block quote for sentences:
  > **저는 한국인이 아니에요.** / I am not a Korean person.
- Use the [OCR ANCHORS] to fix any romanized/garbled Korean from the Whisper audio track.

═══ TEACHING POINTS RULES ═══
- First section MUST be `### Overview`.
- Section titles: descriptive, NO number prefix.  ✓ `### What Is the Possessive Marker 의?`  ✗ `### 1. ...`
- Body is PROSE — continuous paragraphs, NOT bullet or numbered lists.
  Even when the instructor lists 3 rules or 4 steps on screen, you MUST write them out as flowing prose sentences.
  ✓ "The instructor outlines three rules: first, use 존댓말 with strangers; second, minors must use 존댓말 with adults; third, 반말 is reserved for people you know well."
  ✗ "1. With strangers, use 존댓말. 2. If you are a minor..."
  Exception: Korean example sentences, conjugation paradigms, and comparison tables MAY use bullets/tables — but ONLY for the Korean items themselves, not for wrapping explanation text around them.
- **CRITICAL: Do NOT over-summarize or compress. Capture EVERY grammar rule, condition, exception, nuance, example word, and teaching point.**
  If the instructor demonstrates pronunciation of words like "약, 미국, 책", write out the pronunciation for ALL of them, not just 1–2 examples.
  If the instructor lists 7 words that fit a pattern, include ALL 7, not a summary like "and several others."
  This .md is the ONLY source material; omitting details breaks downstream learning.

═══ VISUAL CONTENT — CRITICAL ═══
You are given the actual frames. Integrate ALL on-screen information into the Teaching Points PROSE — nothing visual is ever "optional."
This includes: letter-transformation animations, conjugation charts, on-screen example sentences,
comparison charts, color highlights, and gestures. Silent (무음) on-screen text is teaching content
and MUST be reflected — never skip or omit it.
Example: "The instructor visually demonstrates how 먹다 transforms: 다 is removed, then 어요 is added,
resulting in 먹어요." Do NOT list frames or timestamps separately; weave the visuals into the prose.
**If the screen shows a list of 7 words, mention all 7 in the prose — never compress to "and several others."**

═══ TRANSCRIPT RULES ═══
- Reconstruct the full spoken audio verbatim (English stays English, Korean in Hangul, no translation).
- Remove timestamps; join into natural sentences. Fix romanized Korean using the OCR anchors.
- Format for readability: break into paragraphs at natural topic or section boundaries (every 4–8 sentences).
  Do NOT write the entire transcript as one unbroken wall of text.
- Add this note at the very top of the Transcript section:
  > **Note:** Transcript reconstructed via local Whisper (large-v3) with VAD. May contain minor recognition errors.

═══ CHECKLIST (verify before output) ═══
[ ] Metadata is a bullet list, not a table
[ ] Teaching Points starts with ### Overview
[ ] Section titles have no number prefix, are descriptive
[ ] Body is prose, not bullet explanations
[ ] Korean examples have English glosses; nothing is romanized
[ ] EVERY distinct on-screen state (including silent text slides) is reflected in Teaching Points
[ ] Transcript present, full, verbatim
[ ] No over-summarizing

═══ GOLD-STANDARD EXEMPLARY OUTPUT (match this depth, prose style, Korean handling) ═══
{exemplary}

Output ONLY the raw .md content. No code fences, no preamble, no commentary.
"""


# ──────────────────────── Gemini 호출 ──────────────────────────────────

def _format_duration(seconds) -> str:
    s = int(seconds or 0)
    return f"{s // 60}:{s % 60:02d}"


def call_gemini_sync(client, system_prompt, entry, metadata, timeline,
                     keyframes, anchors, tracker, retry_note=""):
    """동기 Gemini 호출 (executor에서 실행). (text, usage) 반환."""
    from google.genai import types  # 지연 import

    duration_str = metadata.get("duration_string") or _format_duration(metadata.get("duration"))
    upload_raw   = metadata.get("upload_date", "")
    upload_date  = f"{upload_raw[:4]}-{upload_raw[4:6]}-{upload_raw[6:]}" if len(upload_raw) == 8 else upload_raw
    video_title  = metadata.get("title", entry.get("video_title", ""))
    playlist_line = f"Playlist: {entry['playlist']}" if entry["playlist"] else ""
    anchors_str = ", ".join(anchors) if anchors else "(없음)"
    retry_block = ""
    if retry_note:
        retry_block = f"\n\n[RETRY NOTE — CRITICAL]\n{retry_note}\n\nIMPORTANT: The above items MUST be included in your output. Do not compress, omit, or summarize them. Include every example word and teaching point shown on screen."

    intro = f"""[VIDEO METADATA]
Channel: {entry['channel']}
{playlist_line}
URL: {entry['url']}
Duration: {duration_str}
Upload Date: {upload_date}
Mapped Ji Lesson: {entry['lesson_id']} {entry['lesson_title']}
Title: {video_title}

[TIMELINE]
{timeline}
"""

    tail = f"""[OCR ANCHORS]
{anchors_str}

[INSTRUCTION]
Generate the .md per the system prompt. Output the .md content only, no preamble.{retry_block}
"""

    # contents 구성: intro 텍스트 → 프레임 이미지(시간순) → OCR앵커+지시
    contents = [types.Part.from_text(text=intro)]
    for path, _, _ in keyframes:
        try:
            contents.append(types.Part.from_bytes(data=path.read_bytes(), mime_type="image/jpeg"))
        except Exception:
            pass
    contents.append(types.Part.from_text(text=tail))

    cfg_kwargs = dict(system_instruction=system_prompt, temperature=GEMINI_TEMP)
    if THINKING_BUDGET > 0:
        try:
            cfg_kwargs["thinking_config"] = types.ThinkingConfig(thinking_budget=THINKING_BUDGET)
        except Exception:
            pass
    config = types.GenerateContentConfig(**cfg_kwargs)

    for attempt in range(5):
        try:
            resp = client.models.generate_content(model=MODEL_NAME, contents=contents, config=config)
            return resp.text, getattr(resp, "usage_metadata", None)
        except Exception as e:
            msg = str(e)
            if "429" in msg or "RESOURCE_EXHAUSTED" in msg:
                wait = 30 * (2 ** attempt)   # 30, 60, 120, 240, 480초
                logging.warning(f"Gemini 429 → {wait}s 후 재시도 ({attempt+1}/5)")
                time.sleep(wait)
            elif "503" in msg or "UNAVAILABLE" in msg:
                wait = 15 * (2 ** attempt)   # 15, 30, 60, 120, 240초
                logging.warning(f"Gemini 503 → {wait}s 후 재시도 ({attempt+1}/5)")
                time.sleep(wait)
            else:
                raise
    raise RuntimeError("Gemini 503/429: 5회 재시도 소진")


# ──────────────────────── 검증 ─────────────────────────────────────────

# 로마자화 의심 패턴 (v1보다 확장: 실패 파일의 banmal/jondaetmal 등 포함)
_ROMAJA = re.compile(
    r"\b("
    r"imnida|hamnida|haseyo|isseoyo|eobseoyo|opsoyo|juseyo|seumnida|"
    r"banmal|jondaemal|jondaetmal|jondaenmal|nopimmal|nat?chummal|"
    r"annyeong(haseyo)?|kamsahamnida|gamsahamnida|"
    r"seonbae|hubae|oppa|hyung|nuna|unni|dongsaeng|"
    r"ida|hada|meokda|gada|isseo|eoyo|ayo"
    r")\b", re.IGNORECASE)


def validate_md(content: str) -> list:
    errors = []
    if re.search(r"^\|[^|]+\|[^|]+\|", content, re.MULTILINE):
        errors.append("Metadata가 테이블 형식으로 보임")
    if "## Metadata" not in content:
        errors.append("## Metadata 섹션 누락")
    if "### Overview" not in content:
        errors.append("### Overview 누락")
    if "## Transcript" not in content:
        errors.append("## Transcript 섹션 누락")
    if _ROMAJA.search(content):
        errors.append("로마자화 의심 단어 발견")
    # Teaching Points 본문이 불릿 떡칠인지 (산문 규칙 위반) 간이 점검
    tp = content.split("## Teaching Points")[-1].split("## Transcript")[0] if "## Teaching Points" in content else ""
    bullet_lines = len(re.findall(r"^\s*[-*]\s+", tp, re.MULTILINE))
    para_lines = len([l for l in tp.splitlines() if l.strip() and not l.strip().startswith(("#", "-", "*", ">", "|"))])
    if para_lines > 0 and bullet_lines > para_lines * 1.5:
        errors.append("Teaching Points가 산문보다 불릿 위주(산문 규칙 위반 의심)")
    return errors


def coverage_missing(content: str, anchors: list) -> list:
    """화면에 떴던 한글 단어 중 출력 .md에 안 들어간 것 = 시각정보 누락 신호."""
    return [a for a in anchors if a not in content]


# ──────────────────────── 실패 / 복사 / manifest ──────────────────────

def log_failure(url: str, filename: str, reason: str) -> None:
    GEN_DIR.mkdir(parents=True, exist_ok=True)
    with open(FAIL_LOG, "a", encoding="utf-8") as f:
        f.write(f"- **{filename}** (`{url}`): {reason}\n")
    logging.error(f"실패 기록: {filename} — {reason}")


def handle_secondary_copies(source: Path, dests: list) -> list:
    """중복 영상의 나머지 레슨 폴더로 복사. 갱신이 필요한 xlsx row 번호 목록을 반환(호출부에서 O로 갱신)."""
    rows_to_update = []
    for dest_folder, dest_name, dest_entry in dests:
        dest = dest_folder / dest_name
        if not dest.exists():
            dest_folder.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, dest)
            logging.info(f"복사: {source.name} → {dest}")
        if dest_entry.get("status") != "O":
            rows_to_update.append(dest_entry["row"])
    return rows_to_update


# ──────────────────────── 실시간 active_jobs ──────────────────────────
# 현재 처리 중인 영상을 파일로 기록 → 모니터 대시보드가 읽음

_active: dict = {}

def _save_active() -> None:
    GEN_DIR.mkdir(parents=True, exist_ok=True)
    ACTIVE_JOBS.write_text(json.dumps(_active, ensure_ascii=False, indent=2), encoding="utf-8")

def _job_set(label: str, entry: dict, step: int, stage: str) -> None:
    _active[label] = {
        "label": label,
        "lesson_id":    entry.get("lesson_id", ""),
        "lesson_title": entry.get("lesson_title", ""),
        "level":        entry.get("level", ""),
        "step": step,
        "stage": stage,
        "ts": datetime.now().isoformat(timespec="seconds"),
    }
    _save_active()

def _job_clear(label: str) -> None:
    _active.pop(label, None)
    _save_active()


def load_manifest() -> dict:
    if MANIFEST.exists():
        try:
            return json.loads(MANIFEST.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def save_manifest(m: dict) -> None:
    GEN_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(m, ensure_ascii=False, indent=2), encoding="utf-8")


# ──────────────────────── 영상 1개 파이프라인 ─────────────────────────

async def process_video(entry, target_folder, filename, secondary_dests,
                         workers, system_prompt, tracker, manifest):
    url = entry["url"]
    target_path = target_folder / filename
    label = filename[:60]

    if target_path.exists():
        logging.info(f"건너뜀(이미 존재): {label}")
        rows_to_update = handle_secondary_copies(target_path, secondary_dests)
        await update_xlsx_status(entry["row"], "O")
        await update_xlsx_status_many(rows_to_update, "O")
        return True

    if tracker.over_budget():
        raise BudgetExceeded(tracker.summary())

    with tempfile.TemporaryDirectory(prefix="yt2md_") as _tmp:
        tmp = Path(_tmp)
        loop = asyncio.get_event_loop()
        try:
            _job_set(label, entry, 1, "메타데이터 수집")
            logging.info(f"[{label}] 1.메타데이터")
            metadata = await fetch_metadata(url)

            _job_set(label, entry, 2, "영상 다운로드")
            logging.info(f"[{label}] 2.다운로드(480p)")
            video_path = await download_video(url, tmp / "v", workers.dl_sem)

            _job_set(label, entry, 3, "오디오/프레임 분리")
            logging.info(f"[{label}] 3.오디오/프레임 분리")
            audio_path = await loop.run_in_executor(None, lambda: extract_audio_sync(video_path, tmp))
            frames = await loop.run_in_executor(
                None, lambda: extract_frames_sync(video_path, tmp / "frames", INTERNAL_FPS))
            logging.info(f"[{label}] 샘플 프레임 {len(frames)}장")

            _job_set(label, entry, 4, "Whisper 받아쓰기")
            logging.info(f"[{label}] 4.Whisper(VAD)")
            async with workers.gpu_sem:   # GPU 1슬롯
                segments = await loop.run_in_executor(
                    None, lambda: whisper_transcribe_sync(workers.get_whisper(), str(audio_path)))
            if not segments and not frames:
                raise RuntimeError("오디오·화면 모두 비어있음")

            _job_set(label, entry, 5, "키프레임+OCR")
            logging.info(f"[{label}] 5.키프레임 선별+OCR")
            ocr = workers.get_ocr()
            keyframes = await loop.run_in_executor(
                None, lambda: select_keyframes_sync(frames, ocr))
            logging.info(f"[{label}] distinct 프레임 {len(keyframes)}장 보존")

            # 6.타임라인 병합 + 앵커
            timeline = build_timeline(segments, keyframes)
            anchors = collect_korean_anchors(keyframes)

            _job_set(label, entry, 7, "Gemini 합성")
            logging.info(f"[{label}] 7.Gemini 합성")
            await workers.throttle_gemini()
            async with workers.gemini_sem:
                md, usage = await loop.run_in_executor(
                    None, lambda: call_gemini_sync(
                        workers.gemini_client, system_prompt, entry, metadata,
                        timeline, keyframes, anchors, tracker))
            if usage:
                await tracker.add(usage)

            # 7b.검증 (규칙 + 커버리지) → 실패 시 1회 재생성
            errs = validate_md(md)
            missing = coverage_missing(md, anchors)
            if errs or len(missing) > max(2, len(anchors) // 5):
                note = ""
                if errs:
                    note += f"Rule issues: {'; '.join(errs)}. "
                if missing:
                    note += f"These on-screen Korean items are MISSING and must be integrated: {', '.join(missing[:20])}."
                logging.warning(f"[{label}] 검증 보정 재생성: {note[:160]}")
                await asyncio.sleep(5)
                await workers.throttle_gemini()
                async with workers.gemini_sem:
                    md, usage = await loop.run_in_executor(
                        None, lambda: call_gemini_sync(
                            workers.gemini_client, system_prompt, entry, metadata,
                            timeline, keyframes, anchors, tracker, retry_note=note))
                if usage:
                    await tracker.add(usage)
                errs = validate_md(md)
                if errs:
                    # 검증 실패해도 05 Failed output에 보관 (보완 가능성 있음)
                    FAILED_MD_DIR.mkdir(parents=True, exist_ok=True)
                    failed_path = FAILED_MD_DIR / filename
                    failed_path.write_text(md, encoding="utf-8")
                    logging.warning(f"[{label}] 검증 실패 → {FAILED_MD_DIR.name}에 보관: {errs}")
                    log_failure(url, filename, f"재시도 후에도 검증 실패: {errs}")
                    await update_xlsx_status(entry["row"], "F")
                    return False

            # 8.저장
            target_folder.mkdir(parents=True, exist_ok=True)
            target_path.write_text(md, encoding="utf-8")
            rows_to_update = handle_secondary_copies(target_path, secondary_dests)
            manifest[url] = {"filename": filename, "path": str(target_path),
                             "krw": round(tracker.krw, 1),
                             "ts": datetime.now().isoformat(timespec="seconds")}
            await update_xlsx_status(entry["row"], "O")
            await update_xlsx_status_many(rows_to_update, "O")
            _job_clear(label)
            logging.info(f"[{label}] 저장 완료 → {target_path}")
            logging.info(f"[{label}] {tracker.summary()}")
            return True

        except BudgetExceeded:
            _job_clear(label)
            raise
        except Exception as exc:
            _job_clear(label)
            logging.error(f"[{label}] 예외: {exc}", exc_info=True)
            log_failure(url, filename, str(exc))
            return False


# ───────────────────────────── main ──────────────────────────────────

def parse_args():
    ap = argparse.ArgumentParser(description="유튜브 한국어 강의 → .md 변환 (v2)")
    ap.add_argument("--dry-run", action="store_true", help="작업 목록만 출력 (API 호출 없음)")
    ap.add_argument("--limit", type=int, help="앞 N개만")
    ap.add_argument("--level", help="특정 레벨만 (예: 1, Intro)")
    ap.add_argument("--from", dest="lesson_from", help="lesson_id 이상")
    ap.add_argument("--to", dest="lesson_to", help="lesson_id 이하")
    ap.add_argument("--url", help="특정 URL만")
    ap.add_argument("--urls-file", dest="urls_file", help="처리할 URL 목록 파일 (한 줄에 URL 하나)")
    ap.add_argument("--turbo", action="store_true", help="Whisper large-v3-turbo (속도 우선)")
    ap.add_argument("--max-frames", type=int, help=f"영상당 최대 프레임 (기본 {MAX_FRAMES})")
    ap.add_argument("--model", help=f"Gemini 모델 (기본 {MODEL_NAME})")
    ap.add_argument("--budget-krw", type=float, help=f"비용 한도 원화 (기본 {BUDGET_KRW:.0f})")
    return ap.parse_args()


async def main_async():
    global MODEL_NAME, MAX_FRAMES, BUDGET_KRW
    args = parse_args()
    if args.model:
        MODEL_NAME = args.model
    if args.max_frames:
        MAX_FRAMES = args.max_frames
    if args.budget_krw:
        BUDGET_KRW = args.budget_krw

    setup_logging()
    # 이전 실행의 잔여 active_jobs 초기화
    _active.clear()
    _save_active()
    try:
        from dotenv import load_dotenv
        load_dotenv(BASE_DIR / ".env", override=True)
    except Exception:
        pass

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key and not args.dry_run:
        logging.error("GEMINI_API_KEY 없음 (.env 확인)")
        sys.exit(1)

    logging.info(f"BASE_DIR = {BASE_DIR}")
    logging.info(f"xlsx 파싱... ({XLSX_PATH})")
    all_entries = parse_xlsx()
    logging.info(f"xlsx 유튜브 행 전체 {len(all_entries)}개")

    # 변환 대상 = md보유여부가 X(또는 공백)인 행만. O(완료)·F(검증실패, 사람 검토 대기)는 제외.
    # secondary_map(복사 대상 폴더)은 항상 xlsx 전체(all_entries) 기준.
    entries = [e for e in all_entries if e["status"] in ("", "X")]
    logging.info(f"변환 대상(X) {len(entries)}개")
    if args.level:
        entries = [e for e in entries if e["level"] == args.level]
    if args.lesson_from:
        entries = [e for e in entries if e["lesson_id"] >= args.lesson_from]
    if args.lesson_to:
        entries = [e for e in entries if e["lesson_id"] <= args.lesson_to]
    if args.url:
        entries = [e for e in entries if e["url"] == args.url]
    if args.urls_file:
        allowed = set(Path(args.urls_file).read_text(encoding="utf-8").splitlines())
        allowed = {u.strip() for u in allowed if u.strip()}
        entries = [e for e in entries if e["url"] in allowed]

    primary, secondary = build_work_list(entries, all_entries)
    logging.info(f"변환 대상 고유 URL {len(primary)}개")
    if args.limit:
        primary = primary[:args.limit]

    # ── dry-run ──
    if args.dry_run:
        manifest = load_manifest()
        print(f"\n=== DRY RUN ({len(primary)}개) ===\n")
        done = 0
        for entry, folder, fn in primary:
            exists = (folder / fn).exists() or entry["url"] in manifest
            done += exists
            print(f"{'[완료]' if exists else '[대기]'} [row {entry['row']}] {fn}")
            print(f"   URL: {entry['url']}")
            try:
                print(f"   폴더: {folder.relative_to(BASE_DIR)}")
            except ValueError:
                print(f"   폴더: {folder}")
            for sf, sn, se in secondary.get(entry['url'], []):
                print(f"   복사→ [row {se['row']}] {sn}")
        print(f"\n대기 {len(primary)-done} | 완료 {done}")
        print(f"예상 모델: {MODEL_NAME} | 비용 한도: ₩{BUDGET_KRW:,.0f}")
        return

    # ── 실제 실행 ──
    workers = PipelineWorkers()
    if args.turbo:
        workers.whisper_name = "large-v3-turbo"
    workers.init_gemini(api_key)
    system_prompt = build_system_prompt()
    tracker = CostTracker(BUDGET_KRW)
    manifest = load_manifest()

    pipeline_sem = asyncio.Semaphore(PIPELINE_CONC)
    ok = fail = skip = 0
    stop_flag = {"stop": False}

    async def run_one(entry, folder, fn):
        nonlocal ok, fail, skip
        if stop_flag["stop"]:
            return
        url = entry["url"]
        async with pipeline_sem:
            if stop_flag["stop"]:
                return
            if (folder / fn).exists() or url in manifest:
                skip += 1
                src = folder / fn
                if not src.exists() and url in manifest:
                    stored = manifest[url].get("path", "")
                    if stored:
                        src = Path(stored)
                if src.exists():
                    rows_to_update = handle_secondary_copies(src, secondary.get(url, []))
                    await update_xlsx_status(entry["row"], "O")
                    await update_xlsx_status_many(rows_to_update, "O")
                else:
                    logging.warning(
                        f"secondary 복사 불가: {fn} — 원본 없음 "
                        f"(manifest path: {manifest.get(url, {}).get('path', '없음')})"
                    )
                return
            try:
                success = await process_video(entry, folder, fn, secondary.get(url, []),
                                               workers, system_prompt, tracker, manifest)
            except BudgetExceeded as b:
                stop_flag["stop"] = True
                logging.warning(f"비용 한도 도달 → 정지: {b}")
                return
            if success:
                ok += 1
                save_manifest(manifest)   # 성공할 때마다 체크포인트(재개 대비)
            else:
                fail += 1

    await asyncio.gather(*[run_one(e, f, n) for e, f, n in primary])
    save_manifest(manifest)
    logging.info(f"완료. OK={ok} SKIP={skip} FAIL={fail}")
    logging.info(tracker.summary())
    if stop_flag["stop"]:
        logging.warning("비용 한도로 일부 미처리. 충전 후 재실행하면 manifest 기준으로 이어서 진행됨.")


def main():
    asyncio.run(main_async())


if __name__ == "__main__":
    main()

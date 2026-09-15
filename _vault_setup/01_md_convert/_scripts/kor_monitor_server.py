"""
monitor_server.py  v5
변환 현황 브라우저 대시보드 — http://localhost:8765
py -3.12 monitor_server.py

v5: 02_yt_md_convert.xlsx(md보유여부 X/O/F)를 직접 읽어 진행상황을 계산한다.
    (구 커리큘럼맵 .md 파싱 / TOTAL=674 하드코딩 / com1 재시도현황 xlsx는 폐기 — kor_yt_md_pipeline.py와 동일한 입력을 본다.)
"""

import http.server
import json
import os
import re
from datetime import datetime
from pathlib import Path

import openpyxl

SCRIPT_DIR   = Path(__file__).resolve().parent
BASE_DIR     = SCRIPT_DIR.parents[2]  # vault 루트 (<vault>\_vault_setup\01_md_convert\_scripts\ 기준 세 단계 위)
GEN_DIR      = SCRIPT_DIR / "claude_gen"
MANIFEST     = GEN_DIR / "manifest.json"
FAIL_LOG     = GEN_DIR / "변환_실패_log.md"
PROC_LOG     = GEN_DIR / "pipeline_log.txt"
ACTIVE_JOBS  = GEN_DIR / "active_jobs.json"
XLSX_PATH    = BASE_DIR / "01_Raw" / "00_Curriculum_and_index" / "02_yt_md_convert.xlsx"
# 2026-08-31: 04_convert_fail에서 이동. 2026-09-03: 01_inbox에서 _vault_setup\01_md_convert로 이동.
FAILED_MD_DIR = SCRIPT_DIR.parent / "result_check" / "convert_F"

PORT  = 8765

STAGE_KEYS = [
    ("저장 완료",  8, "저장 완료"),
    ("건너뜀",     8, "이미 완료"),
    ("실패 기록",  8, "실패"),
    ("예외:",      8, "실패"),
    ("7.Gemini",   7, "Gemini 합성"),
    ("5.키프레임", 5, "키프레임+OCR"),
    ("4.Whisper",  4, "Whisper 받아쓰기"),
    ("3.오디오",   3, "오디오/프레임 분리"),
    ("2.다운로드", 2, "영상 다운로드"),
    ("1.메타데이터", 1, "메타데이터 수집"),
]

LEVEL_LABEL_MAP = {
    "VSL": "VSL", "Intro": "Intro", "Hangul": "Hangul", "Numbers": "Numbers",
    **{str(i): f"Lv.{i}" for i in range(1, 13)},
}

_LEVEL_ORDER = {"VSL": 0, "Intro": 1, "Hangul": 2, "Numbers": 3}

def _level_order(lv):
    if lv in _LEVEL_ORDER:
        return _LEVEL_ORDER[lv]
    try:
        return 100 + int(lv)
    except (ValueError, TypeError):
        return 99

def _lesson_sort_key(lid):
    parts = lid.split("-", 1)
    base = _level_order(parts[0])
    try:
        return (base, int(parts[1]) if len(parts) > 1 else 0)
    except ValueError:
        return (base, 0)


# ───────── xlsx 파서 (02_yt_md_convert.xlsx — kor_yt_md_pipeline.py와 동일 스키마) ─────────
# 컬럼(0-base): 0 Ji레벨 / 1 Ji레슨 / 2 Ji레슨Title / 3 Raw종류 / 4 채널 / 5 Playlist /
#              6 Ref_No / 7 영상타이틀 / 8 링크 / 9 md보유여부(X/O/F) / 10 추가변환필요여부

def _cell_str(v):
    if v is None:
        return ""
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    return str(v).strip()

def _is_youtube_url(url):
    if not url:
        return False
    if "youtube.com/playlist" in url or "youtube.com/channel" in url:
        return False
    return "youtube.com" in url or "youtu.be" in url

def _make_filename(channel, playlist, video_title):
    parts = [channel]
    if playlist:
        parts.append(playlist)
    parts.append(video_title)
    return re.sub(r'[<>:"/\\|?*\n\r]', "", "_".join(parts) + ".md").strip()

def parse_xlsx():
    """02_yt_md_convert.xlsx 전체 행 파싱. 실패 시 빈 리스트."""
    if not XLSX_PATH.exists():
        return []
    try:
        wb = openpyxl.load_workbook(XLSX_PATH, data_only=True, read_only=True)
        ws = wb[wb.sheetnames[0]]
        entries = []
        for row_idx, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
            if not row:
                continue
            row = list(row) + [None] * (11 - len(row))
            level, lesson_num, lesson_title, _raw_type, channel, playlist, _ref_no, \
                video_title, url, status, _need = row[:11]
            url = _cell_str(url)
            if not url or not _is_youtube_url(url):
                continue
            level_s = _cell_str(level)
            try:
                n = int(float(lesson_num))
                lesson_id = f"{level_s}-{n:02d}"
            except (ValueError, TypeError):
                n = _cell_str(lesson_num)
                lesson_id = f"{level_s}-{n}"
            fn = _make_filename(_cell_str(channel), _cell_str(playlist), _cell_str(video_title))
            entries.append({
                "level": level_s, "lesson_num": n, "lesson_title": _cell_str(lesson_title),
                "lesson_id": lesson_id, "url": url, "filename": fn,
                "status": _cell_str(status).upper(), "row": row_idx,
                "label60": fn[:60],
            })
        wb.close()
        return entries
    except Exception:
        return []


# ───────── 데이터 읽기 ─────────

def load_manifest():
    if not MANIFEST.exists():
        return {}
    try:
        return json.loads(MANIFEST.read_text(encoding="utf-8"))
    except Exception:
        return {}

def load_proc_failures():
    """변환_실패_log.md — 처리 중 예외(다운로드/Whisper/네트워크 등, xlsx 상태는 X로 남아 재시도됨)."""
    if not FAIL_LOG.exists():
        return []
    lines = FAIL_LOG.read_text(encoding="utf-8").splitlines()
    entries = []
    for line in lines:
        if not line.strip().startswith("- **"):
            continue
        m = re.search(r'\(`(https?://[^`]+)`\)', line)
        url = m.group(1) if m else ""
        mf = re.match(r"- \*\*(.+?)\*\*", line)
        filename = mf.group(1) if mf else ""
        entries.append({"line": line, "url": url, "filename": filename})
    return entries

def load_active_jobs(entries):
    """active_jobs.json 있으면 사용, 없거나 비어있으면 로그 파싱 폴백."""
    if ACTIVE_JOBS.exists():
        try:
            data = json.loads(ACTIVE_JOBS.read_text(encoding="utf-8"))
            if data:
                return data
        except Exception:
            pass
    return _active_from_log(entries)

def _active_from_log(entries):
    if not PROC_LOG.exists():
        return {}
    try:
        lines = PROC_LOG.read_text(encoding="utf-8").splitlines()[-3000:]
        cutoff = datetime.now().timestamp() - 900
        recent = []
        for ln in lines:
            try:
                ts = datetime.strptime(ln[:19], "%Y-%m-%d %H:%M:%S").timestamp()
                if ts >= cutoff:
                    recent.append(ln)
            except Exception:
                if recent:
                    recent.append(ln)
        lines = recent if recent else lines[-200:]
    except Exception:
        return {}

    job_state = {}
    for ln in lines:
        m = re.search(r"INFO \[(.+?)\] (.+)$", ln)
        if not m:
            me = re.search(r"ERROR \[(.+?)\]", ln)
            if me:
                label = me.group(1)
                if job_state.get(label, {}).get("step", 0) < 8:
                    job_state[label] = {"step": 8, "stage": "실패"}
            continue
        label, msg = m.group(1), m.group(2)
        for keyword, step, stage_name in STAGE_KEYS:
            if keyword in msg:
                prev = job_state.get(label, {}).get("step", 0)
                if step > prev:
                    job_state[label] = {"step": step, "stage": stage_name}
                break

    label_to_info = {e["label60"]: e for e in entries}
    active = {}
    for label, state in job_state.items():
        if state["step"] >= 8:
            continue
        info = label_to_info.get(label)
        if not info:
            continue
        active[label] = {
            "label": label,
            "lesson_id":    info.get("lesson_id", ""),
            "lesson_title": info.get("lesson_title", ""),
            "level":        info.get("level", "?"),
            "step": state["step"],
            "stage": state["stage"],
        }
    return active


# ───────── HTML 생성 ─────────

def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def stage_dots(step, total=7):
    return "●" * min(step, total) + "○" * max(total - step, 0)

def build_html():
    entries      = parse_xlsx()
    manifest     = load_manifest()
    proc_fails   = load_proc_failures()
    active       = load_active_jobs(entries)

    TOTAL = len(entries)

    # ── 전체 통계 (xlsx md보유여부 컬럼이 유일한 진실 소스: X=대기, O=완료, F=검증실패) ──
    g_done = sum(1 for e in entries if e["status"] == "O")
    g_fail = sum(1 for e in entries if e["status"] == "F")
    g_wait = max(TOTAL - g_done - g_fail, 0)
    g_pct  = (g_done / TOTAL * 100) if TOTAL else 0.0

    # ── 레벨별 집계 ──
    level_data = {}
    for e in entries:
        lv = e["level"]
        d = level_data.setdefault(lv, {"total": 0, "done": 0, "fail": 0})
        d["total"] += 1
        if e["status"] == "O":
            d["done"] += 1
        elif e["status"] == "F":
            d["fail"] += 1
    sorted_levels = sorted(level_data.keys(), key=_level_order)
    lv_stats = {}
    for lv in sorted_levels:
        d = level_data[lv]
        wait = max(d["total"] - d["done"] - d["fail"], 0)
        pct  = (d["done"] / d["total"] * 100) if d["total"] else 0.0
        lv_stats[lv] = {"done": d["done"], "total": d["total"], "fail": d["fail"], "wait": wait, "pct": pct}

    # ── 레슨별 집계 (data-lv 속성으로 필터링) ──
    lesson_groups = {}
    for e in entries:
        lid = e["lesson_id"]
        g = lesson_groups.setdefault(lid, {"title": e["lesson_title"], "level": e["level"], "entries": []})
        g["entries"].append(e)

    all_lesson_rows_html = ""
    for lid in sorted(lesson_groups.keys(), key=_lesson_sort_key):
        g = lesson_groups[lid]
        lv = g["level"]
        n_total = len(g["entries"])
        n_done  = sum(1 for e in g["entries"] if e["status"] == "O")
        n_fail  = sum(1 for e in g["entries"] if e["status"] == "F")
        bar_pct = (n_done / n_total * 100) if n_total else 0.0
        status_note = f' <span class="fbadge">F×{n_fail}</span>' if n_fail else ""
        all_lesson_rows_html += f"""<tr data-lv="{esc(lv)}">
  <td class="lid">{esc(lid)}</td>
  <td class="ltitle">{esc(g['title'])}{status_note}</td>
  <td class="lcount">{n_done}/{n_total}</td>
  <td class="lbar"><div class="lb-bg"><div class="lb-fg" style="width:{bar_pct:.1f}%"></div></div></td>
  <td class="lpct">{bar_pct:.0f}%</td>
</tr>"""

    # ── 레벨 버튼 ──
    btns = '<button class="tab active" data-lv="all" onclick="setLevel(\'all\',this)">전체</button>'
    for lv in sorted_levels:
        lbl = LEVEL_LABEL_MAP.get(lv, lv)
        btns += f'<button class="tab" data-lv="{esc(lv)}" onclick="setLevel(\'{lv}\',this)">{esc(lbl)}</button>'

    # ── 레벨별 stats panel (JS로 show/hide) ──
    panels_html = f"""<div id="panel_all" class="lvpanel">
  <div class="cards">
    <div class="card"><div class="cv">{g_done}</div><div class="cl">완료</div></div>
    <div class="card"><div class="cv">{g_wait}</div><div class="cl">대기</div></div>
    <div class="card"><div class="cv red">{g_fail}</div><div class="cl">검증실패(F)</div></div>
    <div class="card"><div class="cv ora">{g_pct:.1f}%</div><div class="cl">진행률</div></div>
  </div>
  <div class="bar-wrap">
    <div class="bar-lbl">전체 진행률 {g_done}/{TOTAL}</div>
    <div class="bar-bg"><div class="bar-fg" style="width:{min(g_pct,100):.1f}%"></div></div>
  </div>
</div>"""

    for lv in sorted_levels:
        s = lv_stats[lv]
        lbl = LEVEL_LABEL_MAP.get(lv, lv)
        panels_html += f"""<div id="panel_{lv}" class="lvpanel" style="display:none">
  <div class="cards">
    <div class="card"><div class="cv">{s['done']}</div><div class="cl">완료 ({lbl})</div></div>
    <div class="card"><div class="cv">{s['wait']}</div><div class="cl">대기 ({lbl})</div></div>
    <div class="card"><div class="cv red">{s['fail']}</div><div class="cl">검증실패 ({lbl})</div></div>
    <div class="card"><div class="cv ora">{s['pct']:.1f}%</div><div class="cl">진행률 ({lbl})</div></div>
  </div>
  <div class="bar-wrap">
    <div class="bar-lbl">{lbl} 진행률 {s['done']}/{s['total']}</div>
    <div class="bar-bg"><div class="bar-fg" style="width:{min(s['pct'],100):.1f}%"></div></div>
  </div>
</div>"""

    # ── 현재 변환 중 ──
    if active:
        active_html = ""
        for label, job in list(active.items())[:6]:
            lv = job.get("level", "?")
            lvl_label    = LEVEL_LABEL_MAP.get(lv, lv)
            lesson_label = f"{job.get('lesson_id','')}  {job.get('lesson_title','')}"
            step         = job.get("step", 1)
            stage        = job.get("stage", "")
            active_html += f"""<div class="job-card">
  <div class="job-top">
    <span class="job-level">{esc(lvl_label)}</span>
    <span class="job-lesson"> / {esc(lesson_label)}</span>
  </div>
  <div class="job-file">{esc(label)}</div>
  <div class="job-stage"><span class="dots">{stage_dots(step)}</span> 단계 {step}/7 — {esc(stage)}</div>
</div>"""
    else:
        active_html = '<div class="no-active">대기 중 (파이프라인 미실행)</div>'

    # ── 검증 실패(F) — 04_convert_fail 검토 필요 목록 ──
    f_entries = [e for e in entries if e["status"] == "F"]
    fcheck_html = "".join(
        f'<div class="fi"><span class="fl">{esc(e["lesson_id"])}</span> {esc(e["filename"])}</div>'
        for e in f_entries
    ) or '<span class="muted">없음</span>'

    # ── 처리 예외 로그 (다운로드/Whisper 등 — xlsx는 X로 남아 다음 실행에 자동 재시도) ──
    proc_fail_html = "".join(
        f'<div class="fi">{esc(fe["line"][:140])}</div>' for fe in proc_fails[-15:]
    ) or '<span class="muted">없음</span>'

    now = datetime.now().strftime("%H:%M:%S")

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta http-equiv="refresh" content="5">
<title>변환 현황 {g_done}/{TOTAL} ({g_pct:.1f}%)</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#0d1117;color:#e6edf3;font-family:'Consolas','Courier New',monospace;font-size:13px;padding:18px}}
h1{{color:#58a6ff;font-size:1rem;margin-bottom:3px}}
.ts{{color:#8b949e;font-size:.78rem;margin-bottom:10px}}

/* 레벨 탭 */
.tabs{{display:flex;flex-wrap:wrap;gap:5px;margin-bottom:12px}}
.tab{{background:#21262d;border:1px solid #30363d;border-radius:6px;color:#8b949e;
      cursor:pointer;font-family:inherit;font-size:.76rem;padding:4px 10px}}
.tab:hover{{background:#30363d;color:#e6edf3}}
.tab.active{{background:#1f6feb;border-color:#1f6feb;color:#fff;font-weight:bold}}

/* 카드 */
.cards{{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:10px}}
.card{{background:#161b22;border:1px solid #30363d;border-radius:8px;padding:10px 16px;min-width:110px}}
.cv{{font-size:1.6rem;font-weight:bold;color:#58a6ff}}
.cv.red{{color:#f85149}}.cv.ora{{color:#f0883e}}
.cl{{font-size:.72rem;color:#8b949e;margin-top:1px}}

/* 진행 바 */
.bar-wrap{{margin-bottom:14px}}
.bar-lbl{{font-size:.78rem;color:#8b949e;margin-bottom:3px}}
.bar-bg{{background:#21262d;border-radius:4px;height:12px;overflow:hidden}}
.bar-fg{{background:#238636;height:100%;border-radius:4px}}

/* 2단 레이아웃 */
.grid{{display:grid;grid-template-columns:1fr 1.8fr;gap:14px}}
@media(max-width:800px){{.grid{{grid-template-columns:1fr}}}}

.sec{{margin-bottom:14px}}
.sec-t{{color:#f0883e;font-size:.8rem;font-weight:bold;margin-bottom:6px;
        border-bottom:1px solid #21262d;padding-bottom:3px}}

/* 현재 변환 중 카드 */
.job-card{{background:#161b22;border:1px solid #30363d;border-radius:6px;
           padding:9px 12px;margin-bottom:8px}}
.job-top{{margin-bottom:3px}}
.job-level{{color:#58a6ff;font-weight:bold;font-size:.82rem}}
.job-lesson{{color:#8b949e;font-size:.78rem}}
.job-file{{color:#e6edf3;font-size:.76rem;margin-bottom:4px;
           overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
.job-stage{{font-size:.8rem}}
.dots{{color:#3fb950;letter-spacing:1px}}
.no-active{{color:#8b949e;font-size:.82rem;padding:8px 0}}

/* 레슨 테이블 */
.tbl-wrap{{max-height:480px;overflow-y:auto;border:1px solid #21262d;border-radius:6px}}
table{{border-collapse:collapse;width:100%;font-size:.76rem}}
td,th{{padding:3px 6px;border-bottom:1px solid #161b22;vertical-align:middle}}
th{{color:#8b949e;background:#161b22;position:sticky;top:0;z-index:1}}
.lid{{color:#79c0ff;white-space:nowrap;font-size:.72rem}}
.ltitle{{color:#e6edf3;max-width:220px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
.lcount{{text-align:right;white-space:nowrap;color:#8b949e}}
.lbar{{width:80px}}
.lb-bg{{background:#21262d;border-radius:3px;height:8px;overflow:hidden}}
.lb-fg{{background:#238636;height:100%;border-radius:3px}}
.lpct{{text-align:right;color:#3fb950;white-space:nowrap;font-size:.72rem}}
.fbadge{{color:#f85149;font-size:.68rem;border:1px solid #f85149;border-radius:3px;padding:0 4px;margin-left:4px}}

/* 실패 목록 */
.fi{{color:#f85149;font-size:.76rem;padding:2px 0;border-bottom:1px solid #21262d}}
.fl{{color:#79c0ff;margin-right:6px}}
.muted{{color:#8b949e;font-size:.78rem}}

#lesson-header{{color:#f0883e;font-size:.8rem;font-weight:bold;margin-bottom:6px;
                border-bottom:1px solid #21262d;padding-bottom:3px}}
</style>
</head>
<body>
<h1>Korean with Ji — 영상→.md 변환 현황</h1>
<div class="ts">갱신: {now} &nbsp;·&nbsp; 5초 자동 새로고침 &nbsp;·&nbsp; 소스: 02_yt_md_convert.xlsx ({TOTAL}행)</div>

<div class="tabs">{btns}</div>

{panels_html}

<div class="grid">
  <div>
    <div class="sec">
      <div class="sec-t">현재 변환 중</div>
      {active_html}
    </div>
    <div class="sec">
      <div class="sec-t">검증 실패(F) — {FAILED_MD_DIR.name}\\ 검토 필요 ({len(f_entries)}건)</div>
      {fcheck_html}
    </div>
    <div class="sec">
      <div class="sec-t">처리 예외 로그 (자동 재시도 대상)</div>
      {proc_fail_html}
    </div>
  </div>
  <div>
    <div id="lesson-header">레슨별 현황 — 전체</div>
    <div class="tbl-wrap">
      <table>
        <thead><tr><th>레슨</th><th>제목</th><th>완료</th><th>진행률</th><th>%</th></tr></thead>
        <tbody id="lesson-tbody">{all_lesson_rows_html}</tbody>
      </table>
    </div>
  </div>
</div>

<script>
var _cur = 'all';
var _labels = {json.dumps({lv: LEVEL_LABEL_MAP.get(lv, lv) for lv in sorted_levels}, ensure_ascii=False)};
_labels['all'] = '전체';

function setLevel(lv, btn) {{
  document.getElementById('panel_' + _cur).style.display = 'none';
  document.getElementById('panel_' + lv).style.display = '';
  var rows = document.querySelectorAll('#lesson-tbody tr');
  rows.forEach(function(row) {{
    row.style.display = (lv === 'all' || row.dataset.lv === lv) ? '' : 'none';
  }});
  document.getElementById('lesson-header').textContent = '레슨별 현황 — ' + _labels[lv];
  document.querySelectorAll('.tab').forEach(function(b){{ b.classList.remove('active'); }});
  btn.classList.add('active');
  _cur = lv;
  localStorage.setItem('kwj_level', lv);
}}

(function() {{
  var saved = localStorage.getItem('kwj_level') || 'all';
  var btn = document.querySelector('.tab[data-lv="' + saved + '"]');
  if (btn) setLevel(saved, btn);
}})();
</script>
</body>
</html>""".encode("utf-8")


# ───────── 서버 ─────────

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        body = build_html()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    os.chdir(BASE_DIR)
    print(f"대시보드 → http://localhost:{PORT}")
    print("종료: Ctrl+C")
    with http.server.HTTPServer(("", PORT), Handler) as srv:
        srv.serve_forever()

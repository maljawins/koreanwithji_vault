"""Ji Shorts 영상 → 전체 받아쓰기 Markdown.

필요 패키지: faster-whisper, av==16.0.1. 저장된 Whisper large-v3를 로컬에서 사용한다.
직접 실행할 때만 받아쓰기가 시작된다. 기본값은 NVIDIA GPU 사용이다.
영어·한국어를 번역하거나 문장을 다듬지 않는다. 자동 인식 결과는 원음 검토가 필요하다.
"""

import argparse
import os
import re
import site
import sys
from pathlib import Path


VIDEO_DIR = Path(__file__).resolve().parents[1] / "ji_yt_shorts"
OUTPUT_DIR = (Path(__file__).resolve().parents[3]
              / "02_product/02_course_creation/brand_voice/ji_yt_shorts")

# 현재 영상 제목에서 해시태그를 뺀 이름 → 6단어 이하의 요약 제목.
# 긴 제목의 앞부분만 잘라 핵심 내용이나 Part 번호를 잃지 않도록 직접 지정한다.
SHORT_TITLES = {
    "2 Ways to say NO in Korean": "Two Ways to Say No",
    "2 Ways to say THAT in Korean": "Two Ways to Say That",
    "3 Steps Every Kdrama Fan Must Know to Learn Korean with Kdramas": "Three Steps for Learning with Kdramas",
    "3 steps to learn Korean with Kdramas in 2025": "Learn Korean Through Kdramas in 2025",
    "Don't call every Korean guy Oppa 오빠": "Don't Call Every Korean Guy Oppa",
    "How Korean is more simple than English - Verb + 주다 (Give)": "Simplifying Korean with Verb + 주다",
    "How to pronounce ㄹ Korean alphabet ㄹ Is it R or L": "Pronouncing ㄹ Between R and L",
    "How to start learning Korean for free": "Start Learning Korean for Free",
    "Korean curse word with the most uses Part 1": "Versatile Korean Curse Word Part 1",
    "Korean curse word with the most uses Part 2": "Versatile Korean Curse Word Part 2",
    "Korean Particles 은는이가 The only video you need": "Korean Particles 은는이가 Explained",
    "Korean verb ending 군, 구나, 군요 Sentence ending in Korean": "Korean Sentence Endings 군 구나 군요",
    "Korean ㅡ Sound Explained The Ultimate Pronunciation Hack (Part 1)": "Pronouncing Korean ㅡ Part 1",
    "Learn Korean Verb Conjugation Past Tense in 4 Easy Steps": "Korean Past Tense in Four Steps",
    "Polite Korean vs Casual Korean Ignore Formalities with this preposition": "Polite and Casual Korean Formalities",
    "Pronouns in Korean - Gender-neutral": "Gender Neutral Pronouns in Korean",
    "Pronunciation Guide Korean Double Consonants ㄲㄸㅃ": "Pronouncing Korean Double Consonants ㄲㄸㅃ",
    "Pronunciation Guide Korean Double Consonants ㅆㅉ": "Pronouncing Korean Double Consonants ㅆㅉ",
    "The 3-Step Roadmap to Learn Korean in 2025": "Three Step Korean Roadmap for 2025",
    "The Most Common Korean Curse word": "The Most Common Korean Curse Word",
    "The Most Versatile Korean Curse Word": "The Most Versatile Korean Curse Word",
    "This Will Change How You Learn Korean Fundamentals of the Sentence Structure Korean Grammar 101": "Fundamentals of Korean Sentence Structure",
    "What does shibal mean in Korean": "What Does Shibal Mean in Korean",
    "Why I teach Korean and How I teach Korean": "Why and How I Teach Korean",
}


def output_path(video: Path) -> Path:
    """원본 파일명은 유지하고, 받아쓰기 파일의 이름만 정한다."""
    clean_title = " ".join(re.sub(r"#[^\s#]+", "", video.stem).split())
    if clean_title not in SHORT_TITLES:
        raise ValueError(f"새 영상의 요약 제목을 SHORT_TITLES에 추가해야 합니다: {video.name}")
    title = SHORT_TITLES[clean_title]
    if len(title.split()) > 6 or re.search(r'[<>:"/\\|?*#]', title):
        raise ValueError(f"파일명 규칙을 확인하세요: {title}")
    return OUTPUT_DIR / (title + ".md")


def register_gpu_libraries() -> list:
    """이미 설치된 NVIDIA 계산 파일의 위치를 현재 실행에만 연결한다."""
    roots = [Path(site.getusersitepackages()),
             *(Path(p) for p in site.getsitepackages()),
             Path(__file__).resolve().parents[3] / ".venv/Lib/site-packages"]
    handles = []
    for root in roots:
        for folder in (root / "nvidia").glob("*/bin"):
            if folder.is_dir():
                os.environ["PATH"] = str(folder) + os.pathsep + os.environ.get("PATH", "")
                if hasattr(os, "add_dll_directory"):
                    handles.append(os.add_dll_directory(str(folder)))
    return handles


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Ji Shorts 오디오 받아쓰기")
    parser.add_argument("filename", nargs="?", help="영상 파일명. 생략하면 폴더 전체 처리")
    parser.add_argument("--cpu", action="store_true", help="그래픽카드 없이 기본 계산 장치 사용")
    args = parser.parse_args()
    if not VIDEO_DIR.is_dir():
        raise FileNotFoundError(f"영상 폴더가 없습니다: {VIDEO_DIR}")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    videos = sorted(p for p in VIDEO_DIR.iterdir()
                    if p.is_file() and p.suffix.lower() in {".mp4", ".mov", ".mkv", ".webm", ".m4v"})
    if args.filename:
        videos = [video for video in videos if video.name == args.filename]
        if not videos:
            raise FileNotFoundError(f"지정한 영상이 없습니다: {args.filename}")
    jobs = [(video, output_path(video)) for video in videos]
    names = [str(target).casefold() for _, target in jobs]
    if len(names) != len(set(names)):
        raise ValueError("받아쓰기 파일명이 겹칩니다. SHORT_TITLES를 확인하세요.")
    jobs = [(video, target) for video, target in jobs if not target.exists()]
    if not jobs:
        print("새로 받아쓸 영상이 없습니다. 기존 md 파일은 덮어쓰지 않습니다.")
        return

    dll_handles = register_gpu_libraries() if not args.cpu else []
    from faster_whisper import WhisperModel

    model = WhisperModel("large-v3", device="cpu" if args.cpu else "cuda",
                         compute_type="int8" if args.cpu else "float16",
                         local_files_only=True)
    print(f"Whisper device: {model.model.device}; compute: {model.model.compute_type}", flush=True)
    for video, target in jobs:
        print(f"받아쓰기: {video.name}", flush=True)
        segments, _ = model.transcribe(
            str(video),
            task="transcribe",
            beam_size=5,
            vad_filter=True,
            initial_prompt=(
                "Korean language lesson in English and Korean. "
                "Keep English in English and Korean in Hangul. Do not translate."
            ),
        )
        lines = []
        for segment in segments:
            text = segment.text.strip()
            if text:
                if segment.avg_logprob < -1.0:
                    text = "[인식 불확실: 원음 확인 필요] " + text
                lines.append(text)
        if not lines:
            raise RuntimeError(f"인식된 발화가 없습니다. 원음을 확인하세요: {video.name}")
        content = (
            f"# {target.stem}\n\n"
            f"- 원본 영상: {video.name}\n"
            "- 받아쓰기: Whisper large-v3, 번역·문장 교정 없음\n"
            "- 검토 상태: 자동 받아쓰기, 원음 검토 전\n\n"
            "## Transcript\n\n" + "\n\n".join(lines) + "\n"
        )
        with target.open("x", encoding="utf-8") as handle:
            handle.write(content)
        print(f"저장: {target.name}", flush=True)


if __name__ == "__main__":
    main()

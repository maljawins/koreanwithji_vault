"""Prepare only the approved Vinh source locally; no credentials or Gemini calls."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[6]
sys.path.insert(0, str(ROOT / '_vault_setup/01_md_convert/_scripts'))
import teaching_yt_md_pipeline as p

base = ROOT / '_vault_setup/01_md_convert'
state = base / '_scripts/claude_gen/teaching'
args = p.parse_args([])
book = p.load_book(base / 'teaching_yt_md_convert.xlsx')
entry = next(e for e in book.entries if e.vid == 'Sqh6rt1hN2A')
p.check_rows(book, [entry])
guide = (base / 'teaching_yt_md_guide.md').read_text(encoding='utf-8-sig')
with p.execution_lock(state / 'pipeline.lock'):
    media = p.media_folder(entry, args, guide, state)
    media.mkdir(exist_ok=True)
    print('SOURCE WORK:', media, flush=True)
    video, meta = p.download(entry, media, args.max_minutes)
    print('DOWNLOAD VERIFIED:', meta['duration'], 'seconds', flush=True)
    segments = p.transcribe(video, media, args)
    print('TRANSCRIPT:', len(segments), 'segments', flush=True)
    frames = p.select_frames(video, media, meta['duration'], args)
    fingerprint = p.media_fingerprint(media)
    snapshot = media / 'media_snapshot.json'
    if snapshot.exists() and p.read_json(snapshot)['fingerprint'] != fingerprint:
        raise p.PipelineError('Source files changed; review needed')
    if not snapshot.exists():
        p.atomic_json(snapshot, {'fingerprint': fingerprint, 'video_id': entry.vid})
    report = {'source': entry.url, 'duration': meta['duration'], 'media_work': str(media),
              'transcript_segments': len(segments), 'selected_frames': len(frames),
              'gemini_calls': 0, 'document_complete': False, 'workbook_status_unchanged': entry.status}
    p.atomic_json(Path(__file__).parent / 'vinh_local_preparation.json', report)
    print('LOCAL PREPARATION:', report, flush=True)

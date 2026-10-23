"""Read actual artifacts and verify preservation; never use authentication."""
from pathlib import Path
import sys
import json

ROOT = Path(__file__).resolve().parents[6]
sys.path.insert(0, str(ROOT / '_vault_setup/01_md_convert/_scripts'))
import teaching_yt_md_pipeline as p

folder = Path(__file__).parent
state = folder.parent
base = ROOT / '_vault_setup/01_md_convert'
baseline = p.read_json(folder / 'baseline.json')
changes = [name for name, value in baseline.items() if not (ROOT / name).is_file() or p.digest(ROOT / name) != value]
book = p.load_book(base / 'teaching_yt_md_convert.xlsx')
attempts, usage, new_attempts, new_usage = [], [], [], []
for name in ['YZjWuFVSjjM_27c7dba68cb3', 'Sqh6rt1hN2A_ed9082725cec']:
    source = state / name
    for path in source.rglob('calls.jsonl'):
        rows = [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines() if line]
        attempts += rows
        if 'runs' in path.parts:
            new_attempts += rows
    for path in source.rglob('usage.jsonl'):
        rows = [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines() if line]
        usage += rows
        if 'runs' in path.parts:
            new_usage += rows
def totals(rows):
    return {key: sum(row['usage'].get(key) or 0 for row in rows) for key in [
        'prompt_token_count', 'candidates_token_count', 'thoughts_token_count', 'total_token_count']}
manifest = p.read_json(state / 'manifest.json')
results = []
for entry in book.entries:
    record = manifest.get(entry.vid)
    if not record:
        results.append({'video_id': entry.vid, 'workbook_status': entry.status, 'record': None})
        continue
    output = Path(record['output'])
    results.append({'video_id': entry.vid, 'workbook_status': entry.status, 'record': record,
                    'output_matches_record': output.is_file() and p.digest(output) == record['sha256']})
complete = bool(results) and all(item['workbook_status'] == 'O' and item['record']
    and item['record'].get('source_coverage_complete') and item['output_matches_record'] for item in results)
errors = [json.loads(line) for line in (state / 'errors.jsonl').read_text(encoding='utf-8').splitlines() if line] if (state / 'errors.jsonl').exists() else []
latest_attempt = max((item['at'] for item in attempts), default='')
current_error = errors[-1] if errors and errors[-1]['at'] >= latest_attempt else None
status = {
    'checked_at': p.now().isoformat(), 'preserved_baseline_files': len(baseline), 'changed_baseline_files': changes,
    'rows': [p.asdict(entry) for entry in book.entries],
    'new_generate_content_attempts': len(new_attempts), 'new_received_usage_records': len(new_usage),
    'new_reported_usage': totals(new_usage), 'selected_videos_all_attempts_including_history': len(attempts),
    'selected_videos_all_received_usage_records_including_history': len(usage), 'all_recorded_usage_including_history': totals(usage),
    'conversion_complete': complete,
    'blocker': None if complete else current_error,
    'results': results,
    'new_output_files': [item['record']['output'] for item in results if item['record'] and item['record'].get('response_work')],
}
if (folder / 'vinh_local_preparation.json').exists():
    status['vinh_local_preparation'] = p.read_json(folder / 'vinh_local_preparation.json')
p.atomic_json(folder / 'status_snapshot.json', status)
print(json.dumps(status, ensure_ascii=False, indent=2))
if changes:
    raise SystemExit(1)

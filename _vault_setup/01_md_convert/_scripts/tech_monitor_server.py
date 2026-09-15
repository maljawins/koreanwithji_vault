"""
tech_monitor_server.py
Tech 트랙 변환 현황 브라우저 대시보드 — http://localhost:8766
py -3.12 tech_monitor_server.py

kor_monitor_server.py(v5)를 벤치마크해서 tech 트랙 전용으로 새로 썼다. 구조(HTML 생성, 5초
자동 새로고침, 진행 중 job 카드, 실패 목록)는 동일한 방식을 쓰고, 데이터 소스만 갈아 끼웠다.

kor와 다른 점
  - xlsx 스키마: 레벨/레슨 11컬럼이 아니라 자료구분/채널/목적/영상타이틀/링크/변환완료여부 6컬럼
  - 그룹 기준: 레벨·레슨 폴더가 없으므로 대신 xlsx의 "목적" 컬럼으로 묶는다
  - 로그 파일: tech_yt_md_pipeline.py가 쓰는 tech_ 접두어 로그/manifest/active_jobs를 읽는다
  - 포트: kor 대시보드(8765)와 동시에 띄울 수 있도록 8766을 쓴다
  - 파일명에 변환일(YYMMDD)이 들어가므로, 진행 중 job과 xlsx 행을 매칭할 때도 오늘 날짜로 만든
    파일명을 기준으로 삼는다. 다른 날짜에 시작된 작업이 자정을 넘겨 계속 돌고 있으면 라벨이
    어긋날 수 있다 — 그 경우 activity 로그 파싱 쪽 폴백으로 넘어간다(kor와 동일 폴백 구조).
"""

import http.server
import json
import os
import re
from datetime import datetime
from pathlib import Path

import openpyxl

SCRIPT_DIR    = Path(__file__).resolve().parent
BASE_DIR      = SCRIPT_DIR.parents[2]  # vault 루트 (<vault>\_vault_setup\01_md_convert\_scripts\ 기준 세 단계 위)
GEN_DIR       = SCRIPT_DIR / "claude_gen"
MANIFEST      = GEN_DIR / "tech_manifest.json"
FAIL_LOG      = GEN_DIR / "tech_변환_실패_log.md"
PROC_LOG      = GEN_DIR / "tech_pipeline_log.txt"
ACTIVE_JOBS   = GEN_DIR / "tech_active_jobs.json"
XLSX_PATH     = SCRIPT_DIR.parent / "tech_yt_md_convert.xlsx"
# 2026-08-31부터: 성공/실패를 두 폴더로 분리. 2026-09-03: 01_inbox에서 _vault_setup\01_md_convert로 이동.
RESULT_CHECK_DIR = SCRIPT_DIR.parent / "result_check"
INBOX_OUT_DIR    = RESULT_CHECK_DIR / "convert_O"
FAILED_MD_DIR    = RESULT_CHECK_DIR / "convert_F"

PORT = 8766

# tech_yt_md_pipeline.py의 _job_set()/logging 호출과 맞춘 단계 목록.
# 앞쪽부터 매칭하므로 "저장 완료" 등 종료 상태를 먼저 확인해야 한다(kor와 동일 순서 원칙).
STAGE_KEYS = [
    ("저장 완료",   8, "저장 완료"),
    ("건너뜀",      8, "이미 완료"),
    ("실패 기록",   8, "실패"),
    ("예외:",       8, "실패"),
    ("7.Gemini",    7, "Gemini 합성"),
    ("5.키프레임",  5, "키프레임 선별+OCR"),
    ("4.Whisper",   4, "Whisper 받아쓰기"),
    ("3.오디오",    3, "오디오/프레임 분리"),
    ("2.다운로드",  2, "영상 다운로드(1080p)"),
    ("1.메타데이터", 1, "메타데이터 수집"),
]
STAGE_TOTAL = 7  # Gemini 합성이 마지막 진행 단계(8=종료 상태)


# ───────── xlsx 파서 (tech_yt_md_convert.xlsx — tech_yt_md_pipeline.py와 동일 스키마) ─────────
# 컬럼(0-base): 0 자료구분 / 1 채널 / 2 목적 / 3 영상 타이틀 / 4 링크 / 5 변환완료여부

_FORBIDDEN = re.compile(r'[\\/:*?"<>|\x00-\x1f]')
MAX_FILENAME_LEN = 200


def _cell_str(v):
    if v is None:
        return ""
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    return re.sub(r"\s+", " ", str(v)).strip()


def _is_youtube_url(url):
    if not url:
        return False
    if "youtube.com/playlist" in url or "youtube.com/channel" in url:
        return False
    return "youtube.com" in url or "youtu.be" in url


def _sanitize(s):
    s = _FORBIDDEN.sub(" ", s or "")
    s = re.sub(r"\s+", " ", s)
    return s.strip().strip(".")


def _make_filename(channel, video_title, convert_date):
    """tech_yt_md_pipeline.py의 make_filename()과 동일 규칙(금지문자 치환, 200자 절단)."""
    prefix = f"tech_{_sanitize(channel)}_"
    suffix = f"_{convert_date}.md"
    title = _sanitize(video_title)
    room = MAX_FILENAME_LEN - len(prefix) - len(suffix)
    if room < 1:
        prefix = prefix[:MAX_FILENAME_LEN - len(suffix) - 1] + "_"
        room = MAX_FILENAME_LEN - len(prefix) - len(suffix)
    if len(title) > room:
        title = title[:room].rstrip()
    return f"{prefix}{title}{suffix}"


def parse_xlsx():
    """tech_yt_md_convert.xlsx 전체 행 파싱. 실패 시 빈 리스트."""
    if not XLSX_PATH.exists():
        return []
    try:
        wb = openpyxl.load_workbook(XLSX_PATH, data_only=True, read_only=True)
        ws = wb[wb.sheetnames[0]]
        entries = []
        today = datetime.now().strftime("%y%m%d")
        for row_idx, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
            if not row:
                continue
            row = list(row) + [None] * (6 - len(row))
            _kind, channel, purpose, video_title, url, status = row[:6]
            url = _cell_str(url)
            if not url or not _is_youtube_url(url):
                continue
            channel_s = _cell_str(channel)
            title_s = _cell_str(video_title)
            fn = _make_filename(channel_s, title_s, today)
            entries.append({
                "channel": channel_s, "purpose": _cell_str(purpose) or "(목적 없음)",
                "video_title": title_s, "url": url, "filename": fn,
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
    """tech_변환_실패_log.md — 처리 중 예외 또는 검증 실패(xlsx 상태는 F로 갱신됨)."""
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
    """tech_active_jobs.json 있으면 사용, 없거나 비어있으면 로그 파싱 폴백."""
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
            "channel": info.get("channel", ""),
            "purpose": info.get("purpose", ""),
            "step": state["step"],
            "stage": state["stage"],
        }
    return active


# ───────── HTML 생성 ─────────

def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def stage_dots(step, total=STAGE_TOTAL):
    return "●" * min(step, total) + "○" * max(total - step, 0)


def _purpose_key(p):
    return p


def build_html():
    entries    = parse_xlsx()
    manifest   = load_manifest()
    proc_fails = load_proc_failures()
    active     = load_active_jobs(entries)

    TOTAL = len(entries)

    # ── 전체 통계 (xlsx 변환완료여부 컬럼이 유일한 진실 소스: X=대기, O=완료, F=검증실패, 공란=대상 아님) ──
    g_done = sum(1 for e in entries if e["status"] == "O")
    g_fail = sum(1 for e in entries if e["status"] == "F")
    g_target = sum(1 for e in entries if e["status"] in ("X", "O", "F"))
    g_wait = max(g_target - g_done - g_fail, 0)
    g_pct  = (g_done / g_target * 100) if g_target else 0.0
    g_blank = TOTAL - g_target

    # ── 목적별 집계 (레벨 대신 목적으로 묶는다 — tech xlsx에는 레벨·레슨 개념이 없다) ──
    purpose_data = {}
    for e in entries:
        p = e["purpose"]
        d = purpose_data.setdefault(p, {"total": 0, "done": 0, "fail": 0, "blank": 0})
        if e["status"] == "":
            d["blank"] += 1
            continue
        d["total"] += 1
        if e["status"] == "O":
            d["done"] += 1
        elif e["status"] == "F":
            d["fail"] += 1
    sorted_purposes = sorted(purpose_data.keys(), key=_purpose_key)
    p_stats = {}
    for p in sorted_purposes:
        d = purpose_data[p]
        wait = max(d["total"] - d["done"] - d["fail"], 0)
        pct  = (d["done"] / d["total"] * 100) if d["total"] else 0.0
        p_stats[p] = {"done": d["done"], "total": d["total"], "fail": d["fail"],
                      "wait": wait, "pct": pct, "blank": d["blank"]}

    # 탭 id에 못 쓰는 문자(공백 등)를 안전한 키로 치환
    def tab_id(p):
        return re.sub(r"[^0-9A-Za-z_]", "_", p)[:40] or "p"

    # ── 행별 목록 (목적 탭으로 필터링) ──
    all_row_html = ""
    for e in sorted(entries, key=lambda e: (_purpose_key(e["purpose"]), e["row"])):
        badge = {"O": '<span class="okbadge">O</span>', "F": '<span class="fbadge">F</span>',
                 "X": '<span class="xbadge">X</span>'}.get(e["status"], '<span class="blankbadge">공란</span>')
        all_row_html += f"""<tr data-p="{esc(tab_id(e['purpose']))}">
  <td class="stcell">{badge}</td>
  <td class="chcell">{esc(e['channel'])}</td>
  <td class="ttitle">{esc(e['video_title'])}</td>
  <td class="purcell">{esc(e['purpose'])}</td>
</tr>"""

    # ── 목적 버튼 ──
    btns = '<button class="tab active" data-p="all" onclick="setPurpose(\'all\',this)">전체</button>'
    for p in sorted_purposes:
        btns += f'<button class="tab" data-p="{esc(tab_id(p))}" onclick="setPurpose(\'{tab_id(p)}\',this)">{esc(p)}</button>'

    # ── 전체 stats panel + 목적별 panel (JS로 show/hide) ──
    panels_html = f"""<div id="panel_all" class="lvpanel">
  <div class="cards">
    <div class="card"><div class="cv">{g_done}</div><div class="cl">완료</div></div>
    <div class="card"><div class="cv">{g_wait}</div><div class="cl">대기(X)</div></div>
    <div class="card"><div class="cv red">{g_fail}</div><div class="cl">검증실패(F)</div></div>
    <div class="card"><div class="cv ora">{g_pct:.1f}%</div><div class="cl">진행률</div></div>
    <div class="card"><div class="cv muted2">{g_blank}</div><div class="cl">공란(대상 아님)</div></div>
  </div>
  <div class="bar-wrap">
    <div class="bar-lbl">전체 진행률 {g_done}/{g_target} (대상 {g_target}행, 전체 {TOTAL}행)</div>
    <div class="bar-bg"><div class="bar-fg" style="width:{min(g_pct,100):.1f}%"></div></div>
  </div>
</div>"""

    for p in sorted_purposes:
        s = p_stats[p]
        pid = tab_id(p)
        panels_html += f"""<div id="panel_{pid}" class="lvpanel" style="display:none">
  <div class="cards">
    <div class="card"><div class="cv">{s['done']}</div><div class="cl">완료 ({esc(p)})</div></div>
    <div class="card"><div class="cv">{s['wait']}</div><div class="cl">대기 ({esc(p)})</div></div>
    <div class="card"><div class="cv red">{s['fail']}</div><div class="cl">검증실패 ({esc(p)})</div></div>
    <div class="card"><div class="cv ora">{s['pct']:.1f}%</div><div class="cl">진행률 ({esc(p)})</div></div>
  </div>
  <div class="bar-wrap">
    <div class="bar-lbl">{esc(p)} 진행률 {s['done']}/{s['total']}</div>
    <div class="bar-bg"><div class="bar-fg" style="width:{min(s['pct'],100):.1f}%"></div></div>
  </div>
</div>"""

    # ── 현재 변환 중 ──
    if active:
        active_html = ""
        for label, job in list(active.items())[:6]:
            step  = job.get("step", 1)
            stage = job.get("stage", "")
            active_html += f"""<div class="job-card">
  <div class="job-top">
    <span class="job-level">{esc(job.get('channel',''))}</span>
    <span class="job-lesson"> / {esc(job.get('purpose',''))}</span>
  </div>
  <div class="job-file">{esc(label)}</div>
  <div class="job-stage"><span class="dots">{stage_dots(step)}</span> 단계 {step}/{STAGE_TOTAL} — {esc(stage)}</div>
</div>"""
    else:
        active_html = '<div class="no-active">대기 중 (파이프라인 미실행)</div>'

    # ── 검증 실패(F) — convert_fail 검토 필요 목록 ──
    f_entries = [e for e in entries if e["status"] == "F"]
    fcheck_html = "".join(
        f'<div class="fi"><span class="fl">{esc(e["channel"])}</span> {esc(e["filename"])}</div>'
        for e in f_entries
    ) or '<span class="muted">없음</span>'

    # ── 처리 예외 로그 ──
    proc_fail_html = "".join(
        f'<div class="fi">{esc(fe["line"][:140])}</div>' for fe in proc_fails[-15:]
    ) or '<span class="muted">없음</span>'

    now = datetime.now().strftime("%H:%M:%S")

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta http-equiv="refresh" content="5">
<title>Tech 변환 현황 {g_done}/{g_target} ({g_pct:.1f}%)</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#0d1117;color:#e6edf3;font-family:'Consolas','Courier New',monospace;font-size:13px;padding:18px}}
h1{{color:#58a6ff;font-size:1rem;margin-bottom:3px}}
.ts{{color:#8b949e;font-size:.78rem;margin-bottom:10px}}

/* 목적 탭 */
.tabs{{display:flex;flex-wrap:wrap;gap:5px;margin-bottom:12px}}
.tab{{background:#21262d;border:1px solid #30363d;border-radius:6px;color:#8b949e;
      cursor:pointer;font-family:inherit;font-size:.76rem;padding:4px 10px}}
.tab:hover{{background:#30363d;color:#e6edf3}}
.tab.active{{background:#1f6feb;border-color:#1f6feb;color:#fff;font-weight:bold}}

/* 카드 */
.cards{{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:10px}}
.card{{background:#161b22;border:1px solid #30363d;border-radius:8px;padding:10px 16px;min-width:110px}}
.cv{{font-size:1.6rem;font-weight:bold;color:#58a6ff}}
.cv.red{{color:#f85149}}.cv.ora{{color:#f0883e}}.cv.muted2{{color:#6e7681}}
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

/* 행 목록 테이블 */
.tbl-wrap{{max-height:480px;overflow-y:auto;border:1px solid #21262d;border-radius:6px}}
table{{border-collapse:collapse;width:100%;font-size:.76rem}}
td,th{{padding:3px 6px;border-bottom:1px solid #161b22;vertical-align:middle}}
th{{color:#8b949e;background:#161b22;position:sticky;top:0;z-index:1}}
.stcell{{width:36px;text-align:center}}
.chcell{{color:#79c0ff;white-space:nowrap;max-width:120px;overflow:hidden;text-overflow:ellipsis;font-size:.72rem}}
.ttitle{{color:#e6edf3;max-width:320px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
.purcell{{color:#8b949e;white-space:nowrap;font-size:.72rem}}
.okbadge{{color:#3fb950;font-weight:bold}}
.xbadge{{color:#f0883e;font-weight:bold}}
.fbadge{{color:#f85149;font-weight:bold}}
.blankbadge{{color:#6e7681;font-size:.68rem}}

/* 실패 목록 */
.fi{{color:#f85149;font-size:.76rem;padding:2px 0;border-bottom:1px solid #21262d}}
.fl{{color:#79c0ff;margin-right:6px}}
.muted{{color:#8b949e;font-size:.78rem}}

#lesson-header{{color:#f0883e;font-size:.8rem;font-weight:bold;margin-bottom:6px;
                border-bottom:1px solid #21262d;padding-bottom:3px}}
</style>
</head>
<body>
<h1>Tech 트랙 — 영상→.md 변환 현황</h1>
<div class="ts">갱신: {now} &nbsp;·&nbsp; 5초 자동 새로고침 &nbsp;·&nbsp; 소스: tech_yt_md_convert.xlsx ({TOTAL}행)</div>

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
      <div class="sec-t">처리 예외 로그</div>
      {proc_fail_html}
    </div>
  </div>
  <div>
    <div id="lesson-header">영상별 현황 — 전체</div>
    <div class="tbl-wrap">
      <table>
        <thead><tr><th>상태</th><th>채널</th><th>영상 타이틀</th><th>목적</th></tr></thead>
        <tbody id="lesson-tbody">{all_row_html}</tbody>
      </table>
    </div>
  </div>
</div>

<script>
var _cur = 'all';
var _labels = {json.dumps({tab_id(p): p for p in sorted_purposes}, ensure_ascii=False)};
_labels['all'] = '전체';

function setPurpose(p, btn) {{
  document.getElementById('panel_' + _cur).style.display = 'none';
  document.getElementById('panel_' + p).style.display = '';
  var rows = document.querySelectorAll('#lesson-tbody tr');
  rows.forEach(function(row) {{
    row.style.display = (p === 'all' || row.dataset.p === p) ? '' : 'none';
  }});
  document.getElementById('lesson-header').textContent = '영상별 현황 — ' + _labels[p];
  document.querySelectorAll('.tab').forEach(function(b){{ b.classList.remove('active'); }});
  btn.classList.add('active');
  _cur = p;
  localStorage.setItem('kwj_tech_purpose', p);
}}

(function() {{
  var saved = localStorage.getItem('kwj_tech_purpose') || 'all';
  var btn = document.querySelector('.tab[data-p="' + saved + '"]');
  if (btn) setPurpose(saved, btn);
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
    print(f"Tech 대시보드 → http://localhost:{PORT}")
    print("종료: Ctrl+C")
    with http.server.HTTPServer(("", PORT), Handler) as srv:
        srv.serve_forever()

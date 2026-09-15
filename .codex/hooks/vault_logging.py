#!/usr/bin/env python3
"""Codex hooks for this vault's per-turn log and explicit daily close."""

from __future__ import annotations

import json
import os
import sys
import hashlib
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parents[2]
STATE_FILE = (
    Path(tempfile.gettempdir())
    / "koreanwithji-codex-hooks"
    / hashlib.sha256(str(ROOT).encode("utf-8")).hexdigest()[:16]
    / "turns.json"
)
CONVERSATION_LOG = ROOT / "01_inbox" / "conversation_log" / "conversation_log.md"
DAILY_INDEX = ROOT / "00_daily_worklog" / "00_daily_worklog.md"
TODO = ROOT / "01_inbox" / "conversation_log" / "to_do.md"
SEOUL = ZoneInfo("Asia/Seoul")
DAY_CLOSE_WORDS = (
    "오늘 마감",
    "하루 마감",
    "일과 마감",
    "작업 마감",
    "작업 로그 정리",
    "daily worklog 작성",
    "worklog 작성",
)


def read_event() -> dict[str, Any]:
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, OSError):
        return {}
    return data if isinstance(data, dict) else {}


def read_state() -> dict[str, Any]:
    try:
        data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {"turns": {}}
    if not isinstance(data, dict) or not isinstance(data.get("turns"), dict):
        return {"turns": {}}
    return data


def write_state(state: dict[str, Any]) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    temporary = STATE_FILE.with_suffix(".tmp")
    temporary.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(temporary, STATE_FILE)


def prune_turns(state: dict[str, Any]) -> None:
    turns = state["turns"]
    if len(turns) <= 200:
        return
    ordered = sorted(turns.items(), key=lambda item: item[1].get("created_at", ""))
    for turn_id, _ in ordered[:-200]:
        del turns[turn_id]


def now() -> datetime:
    return datetime.now(SEOUL)


def is_daily_close(prompt: str) -> bool:
    normalized = " ".join(prompt.lower().split())
    return any(word in normalized for word in DAY_CLOSE_WORDS)


def marker(turn_id: str) -> str:
    return f"<!-- codex-turn:{turn_id} -->"


def daily_marker(turn_id: str) -> str:
    return f"<!-- codex-day-close:{turn_id} -->"


def contains(path: Path, text: str) -> bool:
    try:
        return text in path.read_text(encoding="utf-8")
    except OSError:
        return False


def write_json(data: dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(data, ensure_ascii=False))


def on_prompt(event: dict[str, Any]) -> None:
    turn_id = str(event.get("turn_id") or "")
    prompt = str(event.get("prompt") or "")
    if not turn_id:
        return

    created = now()
    state = read_state()
    state["turns"][turn_id] = {
        "created_at": created.isoformat(),
        "date": created.strftime("%y%m%d"),
        "permission_mode": str(event.get("permission_mode") or "default"),
        "daily_close": is_daily_close(prompt),
        "status": "pending",
    }
    prune_turns(state)
    write_state(state)

    context = (
        f"Vault log requirement for this turn: before your final answer, append one concise "
        f"entry to `01_inbox/conversation_log/conversation_log.md` with Ji's request, your "
        f"understanding, the work done, and this exact marker: `{marker(turn_id)}`."
    )
    if state["turns"][turn_id]["daily_close"]:
        context += (
            " Ji explicitly requested a daily close. Invoke `$vault-day-close` and complete "
            "that workflow before the final answer."
        )
    write_json(
        {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": context,
            }
        }
    )


def on_stop(event: dict[str, Any]) -> None:
    turn_id = str(event.get("turn_id") or "")
    state = read_state()
    record = state["turns"].get(turn_id)
    if not record:
        return

    mode = str(event.get("permission_mode") or record.get("permission_mode") or "default")
    if mode == "plan":
        record["status"] = "deferred_plan"
        write_state(state)
        write_json({"systemMessage": "Plan mode: vault log enforcement is deferred to an editable turn."})
        return

    missing = []
    if not contains(CONVERSATION_LOG, marker(turn_id)):
        missing.append("the conversation_log entry")

    if record.get("daily_close"):
        date = str(record["date"])
        daily_log = ROOT / "00_daily_worklog" / f"{date}_log" / f"{date}_log.md"
        close_marker = daily_marker(turn_id)
        for label, path in (
            ("the daily log", daily_log),
            ("the daily-worklog index", DAILY_INDEX),
            ("the to_do update", TODO),
        ):
            if not contains(path, close_marker):
                missing.append(label)

    if not missing:
        record["status"] = "complete"
        write_state(state)
        return

    if event.get("stop_hook_active"):
        record["status"] = "unresolved"
        write_state(state)
        write_json(
            {
                "systemMessage": "Vault logging still needs attention. The guard will not loop; resolve it in the next editable turn."
            }
        )
        return

    record["status"] = "blocked_once"
    write_state(state)
    details = ", ".join(missing)
    write_json(
        {
            "decision": "block",
            "reason": (
                f"Before ending, complete {details}. Use the exact turn marker `{marker(turn_id)}`. "
                "If this is a daily close, also use the exact codex-day-close marker in all three required files."
            ),
        }
    )


def main() -> None:
    event = read_event()
    event_name = event.get("hook_event_name")
    if event_name == "UserPromptSubmit":
        on_prompt(event)
    elif event_name == "Stop":
        on_stop(event)


if __name__ == "__main__":
    main()

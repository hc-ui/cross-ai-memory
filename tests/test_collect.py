import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

from aimem.collect import initialize, jsonl_to_messages, normalize_file, scan


def test_normalize_cursor_jsonl(tmp_path: Path) -> None:
    path = tmp_path / "chat.jsonl"
    path.write_text(
        json.dumps(
            {
                "role": "user",
                "message": {
                    "content": [
                        {"type": "text", "text": "remember that the vault is local"},
                        {"type": "tool_use", "name": "Read", "input": {"path": "secret"}},
                    ]
                },
            }
        )
        + "\n",
        encoding="utf-8",
    )
    out = normalize_file(path, "cursor")
    assert "remember that the vault is local" in out
    assert "tool_use" not in out
    assert "SOURCE=cursor" in out


def test_redacts_during_parse() -> None:
    messages = jsonl_to_messages(
        json.dumps({"role": "user", "message": {"content": [{"type": "text", "text": "api_key=sk-abcdefghijklmnopqrstuvwxyz"}]}}) + "\n",
        "cursor",
    )
    assert messages
    assert "sk-abcdefghijklmnopqrstuvwxyz" not in messages[0]["text"]


def test_scan_round_robin(tmp_path: Path) -> None:
    inbox = tmp_path / "inbox"
    cursor_root = tmp_path / "cursor" / "agent-transcripts"
    grok_root = tmp_path / "grok"
    cursor_root.mkdir(parents=True)
    grok_root.mkdir(parents=True)
    old = datetime.now(timezone.utc) - timedelta(minutes=30)

    def write_session(path: Path, text: str) -> None:
        path.write_text(text + "\n", encoding="utf-8")
        path.touch()
        import os

        os.utime(path, (old.timestamp(), old.timestamp()))

    write_session(cursor_root / "a.jsonl", json.dumps({"role": "user", "message": {"content": "hello from cursor"}}))
    write_session(grok_root / "chat_history.jsonl", json.dumps({"type": "user", "content": "hello from grok"}))

    config = {
        "version": 1,
        "sources": [
            {
                "id": "cursor",
                "roots": [str(tmp_path / "cursor")],
                "include": "*.jsonl",
                "required_regex": r"/agent-transcripts/",
                "exclude_regex": "",
            },
            {
                "id": "grok",
                "roots": [str(grok_root)],
                "include": "chat_history.jsonl",
                "required_regex": r"/chat_history\.jsonl$",
                "exclude_regex": "",
            },
        ],
    }
    config_path = inbox / "config.json"
    inbox.mkdir()
    config_path.write_text(json.dumps(config), encoding="utf-8")
    initialize(inbox, config_path)

    write_session(cursor_root / "b.jsonl", json.dumps({"role": "user", "message": {"content": "newer cursor"}}))
    write_session(grok_root / "chat_history.jsonl", json.dumps({"type": "user", "content": "newer grok"}))

    result = scan(inbox, max_items=2, quiet_minutes=5, config_file=config_path)
    sources = {item["source"] for item in result["items"]}
    assert sources == {"cursor", "grok"}
    assert result["selected_count"] == 2

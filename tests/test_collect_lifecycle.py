import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

from aimem.cli import main
from aimem.collect import (
    abandon_scan,
    commit_scan,
    initialize,
    jsonl_to_messages,
    load_config,
    read_item,
    scan,
    status,
    write_json_atomic,
)


def _touch_old(path: Path, text: str, minutes: int = 30) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text + "\n", encoding="utf-8")
    stamp = (datetime.now(timezone.utc) - timedelta(minutes=minutes)).timestamp()
    import os

    os.utime(path, (stamp, stamp))


def _inbox_with_sources(tmp_path: Path) -> tuple[Path, Path, Path]:
    inbox = tmp_path / "inbox"
    cursor_root = tmp_path / "cursor" / "agent-transcripts"
    grok_root = tmp_path / "grok"
    cursor_root.mkdir(parents=True)
    grok_root.mkdir(parents=True)
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
    inbox.mkdir()
    config_path = inbox / "config.json"
    config_path.write_text(json.dumps(config), encoding="utf-8")
    initialize(inbox, config_path)
    return inbox, config_path, cursor_root


def test_collect_read_commit_abandon_and_status(tmp_path: Path) -> None:
    inbox, config_path, cursor_root = _inbox_with_sources(tmp_path)
    _touch_old(cursor_root / "new.jsonl", json.dumps({"role": "user", "message": {"content": "hello"}}))
    created = scan(inbox, max_items=4, quiet_minutes=5, config_file=config_path)
    scan_id = created["scan_id"]
    assert created["selected_count"] == 1
    text = read_item(inbox, scan_id, 0, config_file=config_path)
    assert "hello" in text
    committed = commit_scan(inbox, scan_id)
    assert committed["status"] == "committed"
    again = commit_scan(inbox, scan_id)
    assert again["status"] == "already_committed"
    ready = status(inbox, config_path)
    assert ready["status"] == "ready"
    assert ready["pending_scans"] == 0

    _touch_old(cursor_root / "later.jsonl", json.dumps({"role": "user", "message": {"content": "later"}}))
    second = scan(inbox, max_items=4, quiet_minutes=5, config_file=config_path)
    abandoned = abandon_scan(inbox, second["scan_id"])
    assert abandoned["status"] == "abandoned"
    assert abandon_scan(inbox, second["scan_id"])["status"] == "abandoned"


def test_commit_requires_read(tmp_path: Path) -> None:
    inbox, config_path, cursor_root = _inbox_with_sources(tmp_path)
    _touch_old(cursor_root / "new.jsonl", json.dumps({"role": "user", "message": {"content": "hello"}}))
    created = scan(inbox, max_items=4, quiet_minutes=5, config_file=config_path)
    try:
        commit_scan(inbox, created["scan_id"])
    except ValueError as exc:
        assert "not read" in str(exc)
    else:
        raise AssertionError("unread commit should fail")


def test_scan_rejects_bad_limits(tmp_path: Path) -> None:
    inbox, config_path, _cursor_root = _inbox_with_sources(tmp_path)
    try:
        scan(inbox, max_items=0, config_file=config_path)
    except ValueError:
        pass
    else:
        raise AssertionError("max_items=0 should fail")
    try:
        scan(inbox, quiet_minutes=-1, config_file=config_path)
    except ValueError:
        pass
    else:
        raise AssertionError("quiet_minutes=-1 should fail")


def test_invalid_config_and_state_json(tmp_path: Path) -> None:
    inbox = tmp_path / "inbox"
    inbox.mkdir()
    (inbox / "config.json").write_text("{not-json", encoding="utf-8")
    try:
        load_config(inbox)
    except ValueError as exc:
        assert "invalid JSON" in str(exc)
    else:
        raise AssertionError("bad config should fail")


def test_jsonl_parsers_cover_each_source() -> None:
    samples = {
        "codex": json.dumps(
            {
                "type": "response_item",
                "timestamp": "t",
                "payload": {"type": "message", "role": "user", "content": "from codex"},
            }
        ),
        "claude-code": json.dumps(
            {"type": "user", "timestamp": "t", "message": {"role": "user", "content": "from claude"}}
        ),
        "grok": json.dumps({"type": "user", "content": "from grok"}),
        "antigravity": json.dumps(
            {"source": "USER_EXPLICIT", "type": "USER_INPUT", "created_at": "t", "content": "from antigravity"}
        ),
        "cursor": json.dumps({"role": "assistant", "content": "from cursor"}),
    }
    for source, line in samples.items():
        messages = jsonl_to_messages(line + "\n", source)
        assert messages, source
        assert messages[0]["text"].startswith("from ")


def test_read_rejects_path_outside_allowlist(tmp_path: Path) -> None:
    inbox, config_path, cursor_root = _inbox_with_sources(tmp_path)
    outside = tmp_path / "outside.jsonl"
    _touch_old(outside, json.dumps({"role": "user", "message": {"content": "secret"}}))
    _touch_old(cursor_root / "ok.jsonl", json.dumps({"role": "user", "message": {"content": "ok"}}))
    created = scan(inbox, max_items=4, quiet_minutes=5, config_file=config_path)
    scan_file = inbox / "scans" / f"{created['scan_id']}.json"
    payload = json.loads(scan_file.read_text(encoding="utf-8"))
    payload["items"][0]["path"] = str(outside)
    write_json_atomic(scan_file, payload)
    try:
        read_item(inbox, created["scan_id"], 0, config_file=config_path)
    except ValueError as exc:
        assert "allowlist" in str(exc)
    else:
        raise AssertionError("path outside allowlist should fail")


def test_cli_collect_status(tmp_path: Path, capsys) -> None:
    inbox, config_path, _cursor_root = _inbox_with_sources(tmp_path)
    assert main(["collect", "status", "--inbox", str(inbox), "--config", str(config_path)]) == 0
    assert "ready" in capsys.readouterr().out

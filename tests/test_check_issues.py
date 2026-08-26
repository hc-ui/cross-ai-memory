from datetime import date, timedelta
from pathlib import Path

from aimem.check import check_vault
from aimem.cli import main


REQUIRED = """title: {title}
created: {created}
updated: {updated}
last_confirmed: {confirmed}
source: test
confidence: {confidence}
status: {status}
scope: {scope}
note_type: {note_type}
tags: [test]
"""


def _write(path: Path, *, title: str, note_type: str, body: str = "", **fields: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    block = REQUIRED.format(
        title=title,
        created=fields.get("created", today),
        updated=fields.get("updated", today),
        confirmed=fields.get("last_confirmed", today),
        confidence=fields.get("confidence", "confirmed"),
        status=fields.get("status", "active"),
        scope=fields.get("scope", "shared"),
        note_type=note_type,
    )
    known = {
        "created",
        "updated",
        "last_confirmed",
        "confidence",
        "status",
        "scope",
    }
    extra = "".join(f"{key}: {value}\n" for key, value in fields.items() if key not in known)
    path.write_text(f"---\n{block}{extra}---\n\n{body}\n", encoding="utf-8")


def _codes(vault: Path) -> set[str]:
    return {issue.code for issue in check_vault(vault).issues}


def test_vault_missing(tmp_path: Path) -> None:
    result = check_vault(tmp_path / "nope")
    assert any(issue.code == "VAULT-MISSING" for issue in result.issues)
    assert result.notes == 0


def test_frontmatter_and_field_and_enums(tmp_path: Path) -> None:
    vault = tmp_path / "v"
    vault.mkdir()
    (vault / "bare.md").write_text("no frontmatter\n", encoding="utf-8")
    _write(
        vault / "MEMORY.md",
        title="Entry",
        note_type="index",
        body="[[bad]]",
        status="nope",
        confidence="maybe",
        scope="everywhere",
        created="13-13-13",
    )
    codes = _codes(vault)
    assert "NO-FRONTMATTER" in codes
    assert "BAD-STATUS" in codes
    assert "BAD-CONFIDENCE" in codes
    assert "BAD-SCOPE" in codes
    assert "BAD-DATE" in codes
    assert "BROKEN-LINK" in codes
    assert "ENTRY-MISSING" not in codes


def test_entry_missing_and_unreadable(tmp_path: Path) -> None:
    vault = tmp_path / "v"
    vault.mkdir()
    _write(vault / "note.md", title="Orphan", note_type="canonical")
    (vault / "bin.md").write_bytes(b"\xff\xfe not utf8")
    codes = _codes(vault)
    assert "ENTRY-MISSING" in codes
    assert "UNREADABLE" in codes
    assert "NOT-INDEXED" in codes


def test_duplicate_unreachable_review_and_secret(tmp_path: Path) -> None:
    vault = tmp_path / "v"
    vault.mkdir()
    old = (date.today() - timedelta(days=40)).isoformat()
    due = (date.today() - timedelta(days=1)).isoformat()
    _write(vault / "MEMORY.md", title="Entry", note_type="index", body="[[shared/one]]")
    _write(vault / "shared" / "one.md", title="Same", note_type="canonical")
    _write(vault / "shared" / "two.md", title="Same", note_type="canonical")
    _write(
        vault / "shared" / "snap.md",
        title="Snap",
        note_type="snapshot",
        status="active",
    )
    _write(
        vault / "sessions" / "old.md",
        title="Old chat",
        note_type="session",
        created=old,
        review_after="not-a-date",
    )
    _write(
        vault / "shared" / "due.md",
        title="Due",
        note_type="canonical",
        review_after=due,
    )
    _write(
        vault / "shared" / "secret.md",
        title="Secret",
        note_type="canonical",
        body="token sk-abcdefghijklmnopqrstuvwxyz",
    )
    codes = _codes(vault)
    assert "DUPLICATE-TITLE" in codes
    assert "UNREACHABLE" in codes
    assert "NOT-INDEXED" in codes
    assert "ACTIVE-SNAPSHOT-NO-TTL" in codes
    assert "SUMMARY-OLD" in codes
    assert "BAD-REVIEW-DATE" in codes
    assert "REVIEW-DUE" in codes
    assert "SECRET-LIKE" in codes


def test_cli_check_reports_issues(tmp_path: Path, capsys) -> None:
    vault = tmp_path / "v"
    vault.mkdir()
    assert main(["check", str(vault)]) == 1
    out = capsys.readouterr().out
    assert "ENTRY-MISSING" in out
    assert "issues:" in out


def test_cli_init_refuses_nonempty(tmp_path: Path, capsys) -> None:
    dest = tmp_path / "taken"
    dest.mkdir()
    (dest / "keep.txt").write_text("x", encoding="utf-8")
    assert main(["init", str(dest)]) == 2
    assert "error:" in capsys.readouterr().err

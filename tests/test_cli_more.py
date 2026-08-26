from pathlib import Path

from aimem.cli import main
from aimem.paths import bundled_data, default_inbox, repo_root
from aimem.redact import find_secret_like, redact_sensitive_text


def test_cli_doctor_missing_vault(tmp_path: Path, capsys) -> None:
    missing = tmp_path / "no-vault"
    assert main(["doctor", str(missing)]) == 1
    out = capsys.readouterr().out
    assert "vault missing" in out
    assert "local AI session roots" in out


def test_cli_init_and_check_ok(tmp_path: Path) -> None:
    dest = tmp_path / "vault"
    assert main(["init", str(dest)]) == 0
    assert main(["check", str(dest)]) == 0
    assert (dest / "adapters" / "paste.txt").is_file()


def test_cli_collect_missing_state(tmp_path: Path, capsys) -> None:
    inbox = tmp_path / "empty-inbox"
    inbox.mkdir()
    (inbox / "config.json").write_text('{"version": 1, "sources": [{"id": "cursor", "roots": []}]}', encoding="utf-8")
    assert main(["collect", "status", "--inbox", str(inbox)]) == 2
    assert "error:" in capsys.readouterr().err


def test_bundled_data_and_inbox_defaults() -> None:
    assert bundled_data("starter").is_dir()
    assert bundled_data("adapters", "paste.txt").is_file()
    assert default_inbox().name == "AI-Memory-Inbox"
    assert (repo_root() / "pyproject.toml").is_file()


def test_redact_jwt_aws_and_none() -> None:
    jwt = "header eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0In0.signaturepad"
    out = redact_sensitive_text(jwt)
    assert "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9" not in out
    assert find_secret_like("AKIAIOSFODNN7EXAMPLE") is not None
    assert redact_sensitive_text(None) == ""
    assert find_secret_like("ordinary notebook text") is None

from pathlib import Path

from aimem.check import check_vault
from aimem.cli import main
from aimem.collect import normalize_file
from aimem.paths import repo_root
from aimem.tour import tour_text
from aimem.vault import init_vault


def test_demo_vault_is_healthy() -> None:
    result = check_vault(repo_root() / "examples" / "lin-ke")
    assert result.ok, [f"{item.code}:{item.file}:{item.detail}" for item in result.issues]
    assert result.notes >= 10


def test_init_demo(tmp_path: Path) -> None:
    dest = tmp_path / "demo"
    copied = init_vault(dest, demo=True)
    assert "MEMORY.md" in copied
    assert "shared/install-path.md" in copied
    assert check_vault(dest).ok


def test_tour_mentions_the_three_days() -> None:
    text = tour_text()
    assert "Monday" in text
    assert "install-path" in text
    assert "week-2026-08-24" in text


def test_cli_tour() -> None:
    assert main(["tour"]) == 0


def test_sample_session_normalizes() -> None:
    path = repo_root() / "examples" / "sessions" / "cursor-monday.jsonl"
    out = normalize_file(path, "cursor")
    assert "E:/Apps" in out
    assert "同意写入" in out

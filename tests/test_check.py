from pathlib import Path

from aimem.check import check_vault
from aimem.paths import repo_root
from aimem.vault import init_vault


def test_starter_vault_is_healthy() -> None:
    result = check_vault(repo_root() / "starter")
    assert result.ok, [f"{item.code}:{item.file}:{item.detail}" for item in result.issues]


def test_init_and_missing_field(tmp_path: Path) -> None:
    dest = tmp_path / "vault"
    copied = init_vault(dest)
    assert "MEMORY.md" in copied
    assert "adapters/paste.txt" in copied
    assert "adapters/paste.en.txt" in copied
    result = check_vault(dest)
    assert result.ok

    target = dest / "shared" / "examples" / "preferences.md"
    text = target.read_text(encoding="utf-8")
    target.write_text(text.replace("confidence: confirmed\n", ""), encoding="utf-8")
    broken = check_vault(dest)
    assert any(issue.code == "NO-FIELD" for issue in broken.issues)

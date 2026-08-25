from aimem.cli import main
from aimem.paths import repo_root
from aimem.rule import paste_block


def test_paste_block_mentions_the_gate() -> None:
    zh = paste_block("zh")
    en = paste_block("en")
    assert "同意写入" in zh
    assert "<VAULT>" in zh
    assert "MEMORY.md" in zh
    assert "approve write" in en
    assert "<VAULT>" in en


def test_cli_rule() -> None:
    assert main(["rule"]) == 0
    assert main(["rule", "--lang", "en"]) == 0


def test_paste_files_match_rule() -> None:
    root = repo_root() / "adapters"
    assert root.joinpath("paste.txt").read_text(encoding="utf-8") == paste_block("zh")
    assert root.joinpath("paste.en.txt").read_text(encoding="utf-8") == paste_block("en")

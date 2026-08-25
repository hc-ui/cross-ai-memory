from aimem.cli import main
from aimem.rule import paste_block


def test_paste_block_mentions_the_gate() -> None:
    zh = paste_block("zh")
    en = paste_block("en")
    assert "同意写入" in zh
    assert "MEMORY.md" in zh
    assert "approve write" in en


def test_cli_rule() -> None:
    assert main(["rule"]) == 0
    assert main(["rule", "--lang", "en"]) == 0

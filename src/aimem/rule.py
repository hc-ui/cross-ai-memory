PASTE_ZH = """长期记忆是一个本地 Markdown 文件夹。
先读 MEMORY.md，再只打开索引点名的那几篇。
不要把整个文件夹读完。
除非我明确说「记住 / remember / 同意写入 / approve write」，不要写笔记。
先提最小改动。
不要存 Token、密码、Cookie。
"""

PASTE_EN = """Long-term memory is a local folder of markdown notes.
Start at MEMORY.md. Then open only the notes the index names.
Do not read the whole folder.
Do not write a note unless I explicitly say:
记住 / remember / 同意写入 / approve write.
Propose the smallest change first.
Never store tokens, passwords, or cookies.
"""


def paste_block(lang: str = "zh") -> str:
    return PASTE_EN if lang == "en" else PASTE_ZH

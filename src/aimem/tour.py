from __future__ import annotations

from pathlib import Path

from aimem.paths import demo_vault


DAYS = (
    (
        "Monday · Cursor",
        "周一 · Cursor",
        "Lin Ke: new installers go to E:/Apps.",
        "林可：新软件放到 E:/Apps。",
        "shared/install-path.md",
        "Cursor wrote one note after 同意写入.",
        "Cursor 得到「同意写入」后，只写了这一篇。",
    ),
    (
        "Wednesday · Claude",
        "周三 · Claude",
        "Claude opened MEMORY.md, then the same install-path note.",
        "Claude 先打开 MEMORY.md，再打开同一篇安装路径。",
        "MEMORY.md",
        "It did not ask where files go.",
        "它没有再问文件该放哪。",
    ),
    (
        "Sunday · Codex",
        "周日 · Codex",
        "Codex only wrote a proposal list. One item approved, one rejected, one still open.",
        "Codex 只写了提案清单：一条批准，一条驳回，一条还开着。",
        "proposals/week-2026-08-24.md",
        "Rejected: rewrite the README to get stars.",
        "被驳回的那条：靠改 README 涨星。",
    ),
)


def tour_text(vault: Path | None = None) -> str:
    root = vault or demo_vault()
    lines = [
        "Lin Ke's week  ·  林可的一周",
        "Fictional demo. Steal the shape, not the facts.",
        "虚构演示。抄结构，别抄这些路径当自己的事实。",
        "",
    ]
    for en_day, zh_day, en_said, zh_said, rel, en_end, zh_end in DAYS:
        path = root / rel
        lines.append(en_day)
        lines.append(zh_day)
        lines.append(f"  {en_said}")
        lines.append(f"  {zh_said}")
        lines.append(f"  {path.as_posix() if path.exists() else rel}")
        lines.append(f"  {en_end}")
        lines.append(f"  {zh_end}")
        lines.append("")
    lines.append("Next: aimem check examples/lin-ke")
    lines.append("然后：打开 examples/lin-ke/MEMORY.md")
    return "\n".join(lines) + "\n"

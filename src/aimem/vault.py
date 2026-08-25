from __future__ import annotations

import shutil
from pathlib import Path

from aimem.paths import bundled_data, demo_vault


def init_vault(dest: Path, *, force: bool = False, demo: bool = False) -> list[str]:
    dest = dest.resolve()
    starter = demo_vault() if demo else bundled_data("starter")
    adapters = bundled_data("adapters")
    copied: list[str] = []

    if dest.exists() and any(dest.iterdir()) and not force:
        raise FileExistsError(f"directory is not empty: {dest} (pass --force to merge)")

    dest.mkdir(parents=True, exist_ok=True)
    for src in starter.rglob("*"):
        if src.is_dir():
            continue
        relative = src.relative_to(starter)
        target = dest / relative
        if target.exists() and not force:
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, target)
        copied.append(str(relative).replace("\\", "/"))

    adapter_dir = dest / "adapters"
    adapter_dir.mkdir(parents=True, exist_ok=True)
    for src in adapters.glob("*.md"):
        target = adapter_dir / src.name
        if target.exists() and not force:
            continue
        shutil.copy2(src, target)
        copied.append(f"adapters/{src.name}")
    return copied

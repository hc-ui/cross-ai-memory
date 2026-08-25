from __future__ import annotations

from pathlib import Path


def package_dir() -> Path:
    return Path(__file__).resolve().parent


def repo_root() -> Path:
    return package_dir().parents[1]


def bundled_data(*parts: str) -> Path:
    packaged = package_dir() / "data"
    if parts:
        packaged = packaged.joinpath(*parts)
    if packaged.exists():
        return packaged
    fallback = repo_root().joinpath(*parts)
    if fallback.exists():
        return fallback
    raise FileNotFoundError(f"bundled data not found: {'/'.join(parts)}")


def demo_vault() -> Path:
    packaged = package_dir() / "data" / "demo"
    if (packaged / "MEMORY.md").exists():
        return packaged
    fallback = repo_root() / "examples" / "lin-ke"
    if (fallback / "MEMORY.md").exists():
        return fallback
    raise FileNotFoundError("demo vault not found")


def default_inbox() -> Path:
    return Path.home() / "AI-Memory-Inbox"


def normalize_match_path(path: str | Path) -> str:
    return str(path).replace("\\", "/")

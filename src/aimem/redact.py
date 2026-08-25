from __future__ import annotations

import re

_PATTERNS = (
    (re.compile(r'(?i)(authorization\s*[:=]\s*(?:bearer\s+)?)[^\s"\']+'), r"\1[REDACTED]"),
    (
        re.compile(
            r"(?i)\b(sk-[A-Za-z0-9_-]{16,}|github_pat_[A-Za-z0-9_]{20,}|"
            r"gh[pousr]_[A-Za-z0-9_]{20,}|AIza[A-Za-z0-9_-]{20,})\b"
        ),
        "[REDACTED_TOKEN]",
    ),
    (
        re.compile(r"(?i)\b(eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,})\b"),
        "[REDACTED_JWT]",
    ),
    (
        re.compile(
            r"(?i)((?:api[_-]?key|access[_-]?token|refresh[_-]?token|password|"
            r"passwd|secret|cookie)\s*[:=]\s*)(\"[^\"]*\"|'[^']*'|[^\s,;]+)"
        ),
        r"\1[REDACTED]",
    ),
)


def redact_sensitive_text(text: str | None) -> str:
    if text is None:
        return ""
    value = text
    for pattern, replacement in _PATTERNS:
        value = pattern.sub(replacement, value)
    return value

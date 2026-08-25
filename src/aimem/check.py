from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path

FRONTMATTER_RE = re.compile(r"(?s)^---\r?\n(.*?)\r?\n---")
FIELD_RE = re.compile(r"(?m)^([A-Za-z0-9_]+)[ \t]*:[ \t]*([^\r\n#]*)")
WIKILINK_RE = re.compile(r"\[\[([^\]\[]+?)\]\]")

REQUIRED_FIELDS = (
    "title",
    "created",
    "updated",
    "last_confirmed",
    "source",
    "confidence",
    "status",
    "scope",
    "note_type",
    "tags",
)
VALID_STATUS = {"active", "historical", "deprecated"}
VALID_CONFIDENCE = {"confirmed", "confirmed_for_date", "mixed", "unverified"}
VALID_SCOPE = {"shared", "claude-code", "codex", "grok", "antigravity", "cursor"}
VALID_TYPES = {"index", "canonical", "snapshot", "session", "audit", "readme", "template"}
SECRET_PATTERNS = (
    r"ghp_[A-Za-z0-9]{20,}",
    r"gho_[A-Za-z0-9]{20,}",
    r"github_pat_[A-Za-z0-9_]{20,}",
    r"sk-[A-Za-z0-9]{20,}",
    r"AKIA[0-9A-Z]{16}",
    r"(?i)bearer\s+[A-Za-z0-9\-_\.]{25,}",
    r"(?i)(password|passwd)\s*[:=]\s*\S{6,}",
)
SKIP_DIRS = {".obsidian", ".git", ".aimem-inbox", "__pycache__", ".pytest_cache", "adapters"}


@dataclass
class Issue:
    code: str
    file: str
    detail: str


@dataclass
class CheckResult:
    vault: Path
    notes: int
    issues: list[Issue] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.issues


def _fm_fields(block: str) -> dict[str, str]:
    return {m.group(1): m.group(2).strip() for m in FIELD_RE.finditer(block)}


def _rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def _iter_markdown(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*.md"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        files.append(path)
    return sorted(files)


def _parse_iso_date(value: str) -> date | None:
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


def check_vault(vault: Path) -> CheckResult:
    root = vault.resolve()
    result = CheckResult(vault=root, notes=0)
    if not root.is_dir():
        result.issues.append(Issue("VAULT-MISSING", "", f"vault root not found: {root}"))
        return result

    files = _iter_markdown(root)
    result.notes = len(files)
    targets: dict[str, Path] = {}
    for path in files:
        rel = _rel(path, root)
        targets[rel[:-3]] = path
        targets[path.stem] = path

    records: dict[str, dict[str, str]] = {}
    titles: dict[str, list[str]] = {}
    edges: dict[str, list[str]] = {}
    today = date.today()

    for path in files:
        rel = _rel(path, root)
        text = path.read_text(encoding="utf-8")
        match = FRONTMATTER_RE.match(text)
        if not match:
            result.issues.append(Issue("NO-FRONTMATTER", rel, "frontmatter block missing"))
            continue
        fields = _fm_fields(match.group(1))
        note_type = fields.get("note_type", "")
        for name in REQUIRED_FIELDS:
            if name not in fields:
                result.issues.append(Issue("NO-FIELD", rel, f"missing '{name}'"))

        if note_type != "template":
            status = fields.get("status", "")
            confidence = fields.get("confidence", "")
            scope = fields.get("scope", "")
            if status not in VALID_STATUS:
                result.issues.append(Issue("BAD-STATUS", rel, status))
            if confidence not in VALID_CONFIDENCE:
                result.issues.append(Issue("BAD-CONFIDENCE", rel, confidence))
            if scope not in VALID_SCOPE:
                result.issues.append(Issue("BAD-SCOPE", rel, scope))
            if note_type not in VALID_TYPES:
                result.issues.append(Issue("BAD-NOTE-TYPE", rel, note_type))
            for date_field in ("created", "updated", "last_confirmed"):
                value = fields.get(date_field, "")
                if value and _parse_iso_date(value) is None:
                    result.issues.append(Issue("BAD-DATE", rel, f"{date_field}={value}"))

        review = fields.get("review_after", "")
        if review:
            parsed = _parse_iso_date(review)
            if parsed is None:
                result.issues.append(Issue("BAD-REVIEW-DATE", rel, review))
            elif parsed <= today:
                result.issues.append(Issue("REVIEW-DUE", rel, f"review_after={review}"))

        if fields.get("status") == "active" and note_type == "snapshot" and not review:
            result.issues.append(Issue("ACTIVE-SNAPSHOT-NO-TTL", rel, "active snapshot requires review_after"))

        created = _parse_iso_date(fields.get("created", ""))
        if note_type == "session" and created and "/archive/" not in rel:
            if (today - created).days >= 30:
                result.issues.append(Issue("SUMMARY-OLD", rel, f"age_days={(today - created).days}"))

        title = fields.get("title", "")
        if title:
            titles.setdefault(title, []).append(rel)
        records[rel] = fields
        edges[rel] = []

        for link in WIKILINK_RE.finditer(text):
            raw = link.group(1).split("|", 1)[0].split("#", 1)[0].strip().replace("\\", "/")
            if not raw:
                continue
            target = targets.get(raw)
            if target is None:
                suffix_hits = [path for key, path in targets.items() if key.endswith("/" + raw)]
                target = suffix_hits[0] if len(suffix_hits) == 1 else None
            if target is None:
                result.issues.append(Issue("BROKEN-LINK", rel, raw))
                continue
            edges[rel].append(_rel(target, root))

    for title, paths in titles.items():
        if len(paths) > 1:
            result.issues.append(Issue("DUPLICATE-TITLE", "; ".join(paths), title))

    incoming_from_index: set[str] = set()
    for source, dests in edges.items():
        if records.get(source, {}).get("note_type") == "index":
            incoming_from_index.update(dests)
    for rel, fields in records.items():
        if fields.get("note_type") in {"canonical", "snapshot", "session"} and rel not in incoming_from_index:
            result.issues.append(Issue("NOT-INDEXED", rel, "content note has no incoming link from an index"))

    entry = next((rel for rel, fields in records.items() if Path(rel).name == "MEMORY.md" and fields.get("note_type") == "index"), None)
    if entry is None:
        result.issues.append(Issue("ENTRY-MISSING", "", "MEMORY.md index not found"))
    else:
        visited: set[str] = set()
        queue = [entry]
        while queue:
            node = queue.pop(0)
            if node in visited:
                continue
            visited.add(node)
            queue.extend(edges.get(node, []))
        for rel, fields in records.items():
            if fields.get("note_type") not in {"readme", "template"} and rel not in visited:
                result.issues.append(Issue("UNREACHABLE", rel, "not reachable from MEMORY.md"))

    for path in files:
        rel = _rel(path, root)
        text = path.read_text(encoding="utf-8")
        for pattern in SECRET_PATTERNS:
            if re.search(pattern, text):
                result.issues.append(Issue("SECRET-LIKE", rel, pattern))
                break
    return result

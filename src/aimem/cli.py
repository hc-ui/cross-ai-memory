from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from aimem import __version__
from aimem.check import check_vault
from aimem.collect import (
    abandon_scan,
    commit_scan,
    default_config,
    initialize,
    normalize_file,
    read_item,
    scan,
    source_presence,
    status,
)
from aimem.paths import default_inbox, demo_vault
from aimem.rule import paste_block
from aimem.tour import tour_text
from aimem.vault import init_vault


def _print_json(payload: object) -> int:
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def cmd_init(args: argparse.Namespace) -> int:
    dest = Path(args.path).expanduser()
    copied = init_vault(dest, force=args.force, demo=args.demo)
    kind = "demo vault" if args.demo else "empty vault"
    vault = dest.resolve()
    print(f"{kind} ready: {vault}")
    print(f"copied {len(copied)} files")
    print()
    print("下一步")
    print(f"1. 打开 {vault / 'MEMORY.md'}")
    print("2. 把 adapters/paste.txt 贴进每一家 AI")
    print(f"3. 把规则里的 <VAULT> 换成 {vault}")
    print()
    print("Next")
    print(f"1. open {vault / 'MEMORY.md'}")
    print("2. paste adapters/paste.txt into every AI")
    print(f"3. point <VAULT> at {vault}")
    return 0


def cmd_check(args: argparse.Namespace) -> int:
    result = check_vault(Path(args.path).expanduser())
    print(f"vault: {result.vault}")
    print(f"notes: {result.notes}")
    if result.ok:
        print("ok")
        return 0
    for issue in result.issues:
        print(f"{issue.code}\t{issue.file}\t{issue.detail}")
    print(f"issues: {len(result.issues)}")
    return 1


def cmd_tour(_args: argparse.Namespace) -> int:
    print(tour_text(demo_vault()), end="")
    return 0


def cmd_rule(args: argparse.Namespace) -> int:
    print(paste_block(args.lang), end="")
    return 0


def cmd_doctor(args: argparse.Namespace) -> int:
    vault = Path(args.path).expanduser()
    check_code = 0
    if vault.exists():
        check_code = cmd_check(args)
    else:
        print(f"vault missing: {vault.resolve()}")
        check_code = 1
    print()
    print("local AI session roots")
    for row in source_presence(default_config()):
        found = ", ".join(row["existing_roots"]) if row["existing_roots"] else "(none on this machine)"
        print(f"{row['source']}\t{found}")
    print()
    print("collector never writes the vault. it only proposes.")
    return check_code


def _inbox(args: argparse.Namespace) -> Path:
    return Path(args.inbox).expanduser()


def cmd_collect_init(args: argparse.Namespace) -> int:
    return _print_json(initialize(_inbox(args), Path(args.config) if args.config else None))


def cmd_collect_scan(args: argparse.Namespace) -> int:
    return _print_json(
        scan(
            _inbox(args),
            max_items=args.max_items,
            quiet_minutes=args.quiet_minutes,
            config_file=Path(args.config) if args.config else None,
        )
    )


def cmd_collect_read(args: argparse.Namespace) -> int:
    print(
        read_item(
            _inbox(args),
            args.scan_id,
            args.item_id,
            max_output_chars=args.max_output_chars,
            config_file=Path(args.config) if args.config else None,
        ),
        end="",
    )
    return 0


def cmd_collect_commit(args: argparse.Namespace) -> int:
    return _print_json(commit_scan(_inbox(args), args.scan_id))


def cmd_collect_abandon(args: argparse.Namespace) -> int:
    return _print_json(abandon_scan(_inbox(args), args.scan_id))


def cmd_collect_status(args: argparse.Namespace) -> int:
    return _print_json(status(_inbox(args), Path(args.config) if args.config else None))


def cmd_collect_normalize(args: argparse.Namespace) -> int:
    print(normalize_file(Path(args.path).expanduser(), args.source, max_output_chars=args.max_output_chars), end="")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="aimem",
        description="Human-gated cross-AI memory: init a vault, check it, collect local session candidates.",
    )
    parser.add_argument("--version", action="version", version=f"aimem {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="copy the starter vault")
    init.add_argument("path", nargs="?", default="./my-memory")
    init.add_argument("--force", action="store_true")
    init.add_argument("--demo", action="store_true", help="copy Lin Ke's lived-in notebook instead of the empty starter")
    init.set_defaults(func=cmd_init)

    tour = sub.add_parser("tour", help="print Lin Ke's week: write, read-across, propose")
    tour.set_defaults(func=cmd_tour)

    rule = sub.add_parser("rule", help="print the paste-ready rule for every AI")
    rule.add_argument("--lang", choices=["zh", "en"], default="zh")
    rule.set_defaults(func=cmd_rule)

    check = sub.add_parser("check", help="read-only vault health check")
    check.add_argument("path", nargs="?", default=".")
    check.set_defaults(func=cmd_check)

    doctor = sub.add_parser("doctor", help="check a vault and show which local AI roots exist")
    doctor.add_argument("path", nargs="?", default=".")
    doctor.set_defaults(func=cmd_doctor)

    collect = sub.add_parser("collect", help="scan local AI sessions; never writes the vault")
    collect_sub = collect.add_subparsers(dest="collect_command", required=True)

    def add_inbox(target: argparse.ArgumentParser) -> None:
        target.add_argument("--inbox", default=str(default_inbox()))
        target.add_argument("--config")

    c_init = collect_sub.add_parser("init", help="mark current transcript bytes as baseline")
    add_inbox(c_init)
    c_init.set_defaults(func=cmd_collect_init)

    c_scan = collect_sub.add_parser("scan", help="list new or appended allowlisted files")
    add_inbox(c_scan)
    c_scan.add_argument("--max-items", type=int, default=40)
    c_scan.add_argument("--quiet-minutes", type=int, default=15)
    c_scan.set_defaults(func=cmd_collect_scan)

    c_read = collect_sub.add_parser("read", help="normalize one scan item to user/assistant text")
    add_inbox(c_read)
    c_read.add_argument("--scan-id", required=True)
    c_read.add_argument("--item-id", required=True, type=int)
    c_read.add_argument("--max-output-chars", type=int, default=120000)
    c_read.set_defaults(func=cmd_collect_read)

    c_commit = collect_sub.add_parser("commit", help="advance collector checkpoint only, not git")
    add_inbox(c_commit)
    c_commit.add_argument("--scan-id", required=True)
    c_commit.set_defaults(func=cmd_collect_commit)

    c_abandon = collect_sub.add_parser("abandon", help="drop a pending scan without moving the checkpoint")
    add_inbox(c_abandon)
    c_abandon.add_argument("--scan-id", required=True)
    c_abandon.set_defaults(func=cmd_collect_abandon)

    c_status = collect_sub.add_parser("status")
    add_inbox(c_status)
    c_status.set_defaults(func=cmd_collect_status)

    c_norm = collect_sub.add_parser("normalize", help="normalize one jsonl file without touching inbox state")
    c_norm.add_argument("--path", required=True)
    c_norm.add_argument("--source", required=True, choices=["codex", "claude-code", "grok", "grok-heavy", "antigravity", "cursor"])
    c_norm.add_argument("--max-output-chars", type=int, default=120000)
    c_norm.set_defaults(func=cmd_collect_normalize)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except (FileExistsError, FileNotFoundError, KeyError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

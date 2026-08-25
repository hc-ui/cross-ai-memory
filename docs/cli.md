# CLI reference

This page is for people who already understand the idea and want the commands. If you just landed, start at the [README](../README.md).

Python 3.10+, zero extra packages.

```bash
pip install git+https://github.com/hc-ui/cross-ai-memory.git
aimem tour
aimem check examples/lin-ke
aimem init --demo ./look
aimem doctor ./look
```

| Command | What it does |
| --- | --- |
| `aimem tour` | print Lin Ke's week |
| `aimem rule` | print the paste-ready rule (`--lang zh|en`) |
| `aimem init [DIR]` | copy the empty starter vault and adapters |
| `aimem init --demo [DIR]` | copy the lived-in demo vault |
| `aimem check [DIR]` | read-only health check |
| `aimem doctor [DIR]` | check the vault and list local AI session roots |
| `aimem collect init` | mark current transcript bytes as baseline; no backfill |
| `aimem collect scan` | list new or appended allowlisted files |
| `aimem collect read` | normalize one file to user/assistant text, credentials redacted |
| `aimem collect commit` | advance the collector checkpoint. not a git commit |
| `aimem collect normalize` | parse one jsonl file without touching inbox state |

`collect` never edits the vault.

Windows can also run `tools/Collect-AIMemoryCandidates.ps1`. Same allowlist, same checkpoint idea.

## What the collector reads

Only local session files, and only user / assistant text:

| Source | Default root |
| --- | --- |
| Codex | `~/.codex/sessions`, `~/.codex/archived_sessions` |
| Claude Code | `~/.claude/projects` |
| Grok | `~/.grok/sessions` |
| Grok Heavy | `~/.grok-heavy/sessions` |
| Antigravity | `~/.gemini/antigravity/brain` |
| Cursor | `~/.cursor/projects`, Cursor OD chat folders |

It skips system prompts, tool calls, tool results, reasoning, auth files, settings, caches, attachments, and Codex subagent threads. Files sit for 15 minutes before a scan picks them up. Sources are fair-queued.

Missing roots are skipped. After `aimem collect init`, edit `~/AI-Memory-Inbox/config.json` if your paths differ.

Weekly prompt: `tools/weekly-proposal-prompt.md`.

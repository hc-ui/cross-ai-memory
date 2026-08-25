# cross-ai-memory

You already have six AIs. None of them remember the same things.

`cross-ai-memory` is a **human-gated local memory kit**. Markdown is the source of truth. Agents may propose. They do not write until you say so.

[English](README.md) · [简体中文](README.zh-CN.md)

```text
local session files  ->  collector (read-only)  ->  weekly proposal
                                                    |
                                                    v
                                         you approve a named note
                                                    |
                                                    v
                                         Obsidian / git vault
```

## This is not another memory engine

GitHub already has auto-ingest tools: they embed everything, then inject "relevant" chunks next time.

This kit does the opposite.

| | `cross-ai-memory` | typical agent memory |
| --- | --- | --- |
| Who writes | you, after a proposal | the model, continuously |
| Source of truth | notes you can open | vectors / a graph DB |
| Across AIs | local files from several CLIs | usually one product |
| Vendor hidden memory | not read, not synced | often treated as truth |
| Failure mode | a missed note | silent wrong memory |

It is closer to a filing rule than to Mem0.

## 60 seconds

Python 3.10+, zero dependencies. Not on PyPI yet:

```bash
pip install git+https://github.com/hc-ui/cross-ai-memory.git
aimem init ./my-memory
aimem check ./my-memory
```

Then paste `my-memory/adapters/cursor.md` (or the Claude / Codex file) into that AI's rule file. Point `<VAULT>` at `my-memory`.

Ask the agent a question that needs an old decision. It should open `MEMORY.md`, then one or two notes — not the whole folder.

Say `记住` or `approve write` only when you want a note created.

## Commands

| Command | What it does |
| --- | --- |
| `aimem init [DIR]` | copy the starter vault + adapters |
| `aimem check [DIR]` | read-only health check |
| `aimem doctor [DIR]` | check the vault and list local AI roots that exist |
| `aimem collect init` | mark current transcript bytes as baseline; no backfill |
| `aimem collect scan` | list new or appended allowlisted files |
| `aimem collect read` | normalize one file to user/assistant text, credentials redacted |
| `aimem collect commit` | advance the collector checkpoint. not a git commit |
| `aimem collect normalize` | parse one jsonl file without touching inbox state |

`collect` never edits the vault.

Windows users can run the original PowerShell collector in `tools/Collect-AIMemoryCandidates.ps1`. Same allowlist, same checkpoint idea.

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

It skips system prompts, tool calls, tool results, reasoning, auth files, settings, caches, attachments, and Codex subagent threads. Files must sit still for 15 minutes before a scan picks them up. Sources are fair-queued so one busy AI cannot fill the whole batch.

Missing roots are skipped. Edit `~/AI-Memory-Inbox/config.json` after `aimem collect init` if your paths differ.

## Approval phrases

| You say | Agent may | Agent may not |
| --- | --- | --- |
| `同意写入` / `approve write` | edit named notes, `aimem check`, local commit | push |
| `同意推送` / `approve push` | ordinary push of checked commits | force push |
| `同意写入并推送` / `approve write and push` | both, stop if check fails | skip the check |

A weekly job should only print a list. Use `tools/weekly-proposal-prompt.md`.

## Privacy

- Local only. No API key. No cloud memory service.
- The inbox stores checkpoints, not raw chats.
- Likely tokens are replaced with `[REDACTED]` before a proposal is built. That is not a proof that every secret was found.
- Do not publish a vault that contains real personal notes. This repository ships an example vault only.

## License

[MIT](LICENSE)

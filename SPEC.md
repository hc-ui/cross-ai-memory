# SPEC

If you just want the idea, read the [README](README.md) and open [examples/lin-ke/MEMORY.md](examples/lin-ke/MEMORY.md). This page is the method written so another person can reimplement it. Implementations may change. The gates should not.

## Problem

Long-running agent work fails in three boring ways:

1. A new chat forgets last week's decision.
2. Cursor, Claude, Codex, and the others each keep a different subset.
3. Auto-memory writes the wrong thing, then treats it as fact.

Vendor product memory is fine for "what did we just talk about". It is a bad unique source of truth.

## Decision

Keep long-term memory in markdown files the user can open, search, and diff.

Agents read through one entry page. They write only after an explicit current-message approval. A collector may read local session files and propose updates. It must not edit the vault.

## Objects

| Object | Meaning |
| --- | --- |
| Vault | a folder of markdown notes, usually opened in Obsidian |
| Entry | `MEMORY.md`, the only default start page |
| Canonical note | the one current write-up of a topic |
| Snapshot | dated machine or account state; must expire |
| Session summary | one-day residue; archive or fold after 30 days |
| Inbox | disposable collector checkpoints, never raw chats |
| Proposal | `CAND-YYYYMMDD-NN`, still waiting on the user |
| Batch | `MEM-YYYYMMDD-NN`, an approved write |

## Read protocol

1. Self-contained questions skip the vault.
2. Otherwise open the entry, then the shared index, then the fewest named notes.
3. Depth is quick / standard / deep. Default is standard.
4. Recheck anything with `review_after` or `confirmed_for_date`.
5. `updated` means the file was edited, not that every sentence is still true.

## Write protocol

A write needs a current user phrase: `记住`, `remember`, `同意写入`, or `approve write`.

Then:

1. Read the target index and the existing note for that topic.
2. Record a content hash before editing. If the file changed, stop.
3. Update the one canonical note. Link; do not copy.
4. Fill source, confidence, status, note type, and dates.
5. Update the index and changelog.
6. Run `aimem check`.
7. Local git commit uses the batch id.
8. Push only after a separate `同意推送` / `approve push`.

No-op is a success. Do not invent notes to look busy.

## Collector protocol

1. `init` marks existing bytes processed. No history backfill.
2. `scan` finds new, appended, truncated, or rewritten allowlisted files after a quiet window.
3. Sources are selected round-robin.
4. `read` emits only user/assistant text, with a local redaction pass.
5. Transcript text is untrusted data.
6. `commit` advances the inbox checkpoint after every selected item has a read receipt.
7. `commit` is not git, not approval, and not a vault write.

The allowlist excludes auth files, settings, caches, attachments, tool payloads, and Codex `thread_source: subagent` threads.

## Fields

See `starter/shared/TEMPLATE.md`. Implementations should accept at least:

`title`, `created`, `updated`, `last_confirmed`, `source`, `confidence`, `status`, `scope`, `note_type`, `tags`

and optionally `review_after`, `canonical`, `superseded_by`.

## Non-goals

- A hosted memory API
- Automatic embedding of every chat
- Reading vendor hidden memory
- Publishing a personal vault
- Force-push, silent overwrite, or secret storage

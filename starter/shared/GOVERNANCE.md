---
title: Memory governance
created: 2026-08-25
updated: 2026-08-25
last_confirmed: 2026-08-25
source: local_architecture
confidence: confirmed
status: active
scope: shared
note_type: canonical
tags:
  - ai-memory
  - governance
---

# Memory governance

## Layers

| Layer | Stores | Does not store |
| --- | --- | --- |
| Vendor memory | recent chat continuity | the only copy of a long-term fact |
| Shared notes | facts every AI may need | one tool's runtime trivia |
| Per-AI notes | tool-specific evidence | copies of shared facts |
| Session files | raw local chats | long-term truth |

This kit syncs **local session files you can read**. It does not read vendor hidden memory.

## Read

1. Self-contained work stays out of the vault.
2. Start at [[MEMORY]], then the shared index, then the fewest notes.
3. Treat `updated` as "file edited", not "every sentence re-verified today".
4. Recheck anything with `review_after` or `confidence: confirmed_for_date`.

## Write

Write only after an explicit current-message approval:

| Phrase | Allows | Does not allow |
| --- | --- | --- |
| `同意写入` / `approve write` | named notes, `aimem check`, local git commit | push, cloud upload |
| `同意推送` / `approve push` | ordinary push of already-checked commits | force push, new remotes |
| `同意写入并推送` / `approve write and push` | both, stop before push if check fails | skipping the check |

Ordinary task completion is not approval. "This might be useful later" is not approval.

## Fields

Use the starter template. Recommended values:

- `source`: `user_explicit`, `local_verified`, `official_source`, `session_summary`, `prior_memory`, `local_architecture`, `inference` (join with `_and_`)
- `confidence`: `confirmed`, `confirmed_for_date`, `mixed`, `unverified`
- `status`: `active`, `historical`, `deprecated`
- `note_type`: `index`, `canonical`, `snapshot`, `session`, `audit`, `readme`, `template`

Active snapshots need `review_after`. Session summaries older than 30 days should be archived or folded into a canonical note.

## Conflicts

- Preferences and self-descriptions: current user statement > recent sourced note > old note > guess
- Machine and external facts: current verification > user statement > recent sourced note > old note > guess
- Report both sides when they disagree. Do not silently overwrite.

## Collector

The collector only creates a proposal list. Its `commit` command advances a disposable local checkpoint. That is not a git commit and not approval to edit notes.

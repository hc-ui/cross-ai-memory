---
title: Lin Ke governance
created: 2026-08-11
updated: 2026-08-24
last_confirmed: 2026-08-24
source: local_architecture
confidence: confirmed
status: active
scope: shared
note_type: canonical
tags:
  - demo
  - governance
---

# Governance

## Conclusion

Every AI reads this vault. None of them write it unless Lin Ke says so in the current message.

## The three rules

1. Durable facts live in markdown Lin Ke can open.
2. Cursor, Claude, and Codex all start at [[MEMORY]].
3. A model may add a line to [[proposals/week-2026-08-24]]. It may not edit a canonical note first.

## Approval

| Phrase | Allows |
| --- | --- |
| `同意写入` / `approve write` | named notes, `aimem check`, local commit |
| `同意推送` / `approve push` | ordinary push of checked commits |

"This might be useful later" is not approval.

## Conflicts

- Preferences: current Lin Ke statement > old note
- Machine facts: what we just verified > what an AI remembers
- If they disagree, keep both sentences and mark the boundary. Do not silently overwrite.

## Scope

This page is the demo's rule file. A real vault should keep the same gates and change the facts.

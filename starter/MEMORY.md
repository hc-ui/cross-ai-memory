---
title: Memory entry
created: 2026-08-25
updated: 2026-08-25
last_confirmed: 2026-08-25
source: local_architecture
confidence: confirmed
status: active
scope: shared
note_type: index
tags:
  - ai-memory
  - navigation
---

# Memory entry

This file is the only start page. Agents do not browse the whole vault.

## When to read

1. Self-contained questions do not read the vault.
2. Long-term preferences, old decisions, local paths, or continuing a previous project: read [[shared/INDEX]], then only the notes it points to.
3. Do not load every note. Default depth is **standard**.

## Read depth

| Depth | When | What to open |
| --- | --- | --- |
| quick | one fact | this page plus one note |
| standard | continue a project or check an old decision | the shared index plus one or two notes it names |
| deep | user says "look thoroughly", conflict, new machine | opposing notes and the latest changelog |

## Write gate

Do not write the vault unless the current user message explicitly says to remember, sync, update, or write memory.

- Propose first.
- One canonical note per topic.
- Never store tokens, passwords, cookies, or unnecessary private data.
- Current user statements beat old notes. Verified facts beat guesses. Report conflicts; do not silently overwrite.

Full rules: [[shared/GOVERNANCE]]

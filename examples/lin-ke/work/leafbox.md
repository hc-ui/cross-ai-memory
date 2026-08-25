---
title: Lin Ke leafbox decisions
created: 2026-08-20
updated: 2026-08-22
last_confirmed: 2026-08-22
source: user_explicit_and_local_verified
confidence: mixed
status: active
scope: shared
note_type: canonical
tags:
  - demo
  - project
---

# leafbox

`leafbox` is a fictional CLI that prints a folder tree as one text file. It is not a real product.

## Conclusion

Stdout is UTF-8. Do not emit GBK. A Windows console that shows mojibake is a console problem, not a reason to change the tool.

## Evidence

- 2026-08-20, Cursor, `同意写入`: first note said "use GBK on Windows so the demo looks right".
- 2026-08-22, Claude, `同意写入`: Lin Ke opened a real `cmd.exe`, saw the GBK build break a pipe into Python, and reversed it.
- Still uncertain: none for encoding. The first decision is kept below so the next AI does not revive it.

## What we already rejected

GBK-for-Windows. If a new chat proposes it, point here. Do not reopen the debate unless Lin Ke brings new evidence.

## Scope

Only this fictional project. Installer paths stay in [[shared/install-path]].

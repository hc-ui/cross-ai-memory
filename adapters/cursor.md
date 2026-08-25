# Cursor adapter

Paste this into a Cursor user rule, or save it as `AGENTS.md` in the vault folder. Change the path.

```text
Cross-session memory lives in a local markdown vault, not in vendor memory.

Entry file: <VAULT>/MEMORY.md
Shared index: <VAULT>/shared/INDEX.md

Read:
- Self-contained questions do not open the vault.
- Continuing a project, checking an old decision, or using a local path: read MEMORY.md, then the shared index, then only the notes it names.
- Default depth is standard. Do not open every note.

Write:
- Do not edit the vault unless the current user message explicitly says to remember, sync, update, or write memory.
- Propose the smallest change first. One canonical note per topic.
- After an approved write, run `aimem check <VAULT>` before any git commit.
- `同意写入` / `approve write` allows notes + check + local commit. It does not allow push.
- `同意推送` / `approve push` allows an ordinary push of already-checked commits.
- Never store tokens, passwords, cookies, or unnecessary private data.

Conflicts:
- Current user statements beat old notes.
- Verified machine facts beat guesses.
- Report conflicts. Do not silently overwrite.
```

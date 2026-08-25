# Claude Code adapter

Add this block to `CLAUDE.md` or a Claude skill that always loads. Change the path.

```text
Long-term memory is the local vault at <VAULT>/MEMORY.md.

Do not treat Claude's product memory as the only source of truth.
Do not read the whole vault. Start at MEMORY.md, then shared/INDEX.md, then the fewest notes.

Write only after an explicit current-message approval:
remember / 记住 / 同意写入 / approve write.

After writing, run `aimem check <VAULT>`.
Push only after 同意推送 / approve push.
Do not store credentials or private data.
```

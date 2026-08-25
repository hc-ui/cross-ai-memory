# Steal it tonight

No install. You do not need to read the whole repository.

1. Make a local folder. Save [MEMORY.en.md](https://hc-ui.github.io/cross-ai-memory/MEMORY.en.md) as UTF-8 `MEMORY.md`, not `.txt`.
2. Change that path on the [public page](https://hc-ui.github.io/cross-ai-memory/en.html) and copy the filled rule.
3. Paste the same block into Cursor user rules, Claude `CLAUDE.md`, and Codex `AGENTS.md`.
4. In a new chat, paste the probe on the public page. It should read “Start here”.

When a durable fact should land, say `记住` or `approve write`. It should propose first. You nod, then it writes.

Want the empty shell or Lin Ke’s notebook later:

```bash
pip install git+https://github.com/hc-ui/cross-ai-memory.git
aimem init ./my-memory
aimem init --demo ./look
```

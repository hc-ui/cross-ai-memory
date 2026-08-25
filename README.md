# One notebook for every AI you use

[English](README.md) · [简体中文](README.zh-CN.md)

You told Cursor the download folder this morning.
Tonight Claude asks again.
Next week Codex has never heard of it.

The models are not stupid. Each product keeps its own memory, and that memory is usually a black box. More people will use AI. More people will use **more than one** AI. That gap gets worse, not better.

This repository is a method you can copy:

**Write the durable facts in notes you can open. Point every AI at the same notes. Let the model propose. You approve the write.**

![Three AIs forget separately; one shared notebook remembers after you approve](assets/idea.svg)

## The idea, three sentences

1. Long-term memory lives in **markdown you can open**, not in a vendor's hidden brain.
2. **Every AI reads the same folder.** Cursor, Claude, Codex, Grok — one notebook.
3. **An AI may propose. It does not write until you say so.** Wrong memory should not become "fact".

That is the whole invention. The CLI is optional. If you only steal these three rules, you already have the system.

## Why not "just let the AI remember"

Most memory tools ingest everything, embed it, and inject "relevant" chunks later. That is convenient. It is also how a wrong guess becomes next week's truth.

This method fails in a boring way: you forget to write a note.
Auto-memory fails in a dangerous way: it writes the wrong note, then defends it.

Vendor memory is fine for "what did we just talk about".
It is a bad unique source of truth across chats, tools, and weeks.

## Steal it without installing

Paste this into every AI's rule file. Change the folder path.

```text
Long-term memory is a local folder of markdown notes.
Start at MEMORY.md. Then open only the notes the index names.
Do not read the whole folder.
Do not write a note unless I explicitly say:
记住 / remember / 同意写入 / approve write.
Propose the smallest change first.
Never store tokens, passwords, or cookies.
```

One topic, one note. Current user statements beat old notes. Verified facts beat guesses. If two notes disagree, say so — do not silently overwrite.

The starter vault in this repo is that folder, already shaped.

## Try the kit

```bash
pip install git+https://github.com/hc-ui/cross-ai-memory.git
aimem init ./my-memory
aimem check ./my-memory
```

Point `<VAULT>` in `my-memory/adapters/cursor.md` (or the Claude / Codex file) at that folder. Ask a question that needs last week's decision. The agent should open `MEMORY.md`, then one or two notes — not the whole tree.

Say `记住` only when you want a note created.

Commands, collector paths, and the weekly proposal job: [docs/cli.md](docs/cli.md).
The durable rules: [SPEC.md](SPEC.md).

## What this is not

- Not a cloud memory API
- Not an embedding database
- Not a sync of ChatGPT / Claude / Cursor product memory
- Not someone else's private notes — this repo ships an empty example vault

Local only. No API key.

## License

[MIT](LICENSE)

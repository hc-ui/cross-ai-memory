# One notebook for every AI you use

[![CI](https://github.com/hc-ui/cross-ai-memory/actions/workflows/ci.yml/badge.svg)](https://github.com/hc-ui/cross-ai-memory/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

**Share this page:** [hc-ui.github.io/cross-ai-memory](https://hc-ui.github.io/cross-ai-memory/)

[English](README.md) · [简体中文](README.zh-CN.md) · [English site](https://hc-ui.github.io/cross-ai-memory/en.html)

You told Cursor the download folder this morning.
Tonight Claude asks again.
Next week Codex has never heard of it.

The models are not stupid. Each product keeps its own memory, and that memory is usually a black box. More people will use AI. More people will use **more than one** AI. That gap gets worse, not better.

**Write the durable facts in notes you can open. Point every AI at the same notes. Let the model propose. You approve the write.**

Share this first:

```text
One notebook for every AI. Agents propose. You approve.
https://hc-ui.github.io/cross-ai-memory/
```

![Without a shared notebook Claude asks again; with one it continues](assets/chat.svg)

## Don't read about it. Open the notebook.

[examples/lin-ke/MEMORY.md](examples/lin-ke/MEMORY.md) is a **fictional** vault that is already in use. Lin Ke is not a real person. The files are real.

| Open this | What happens in the story |
| --- | --- |
| [install-path.md](examples/lin-ke/shared/install-path.md) | Monday: Cursor writes `E:/Apps` after `同意写入` |
| [MEMORY.md](examples/lin-ke/MEMORY.md) | Wednesday: Claude starts here and does not ask again |
| [week-2026-08-24.md](examples/lin-ke/proposals/week-2026-08-24.md) | Sunday: Codex only proposes |
| [leafbox.md](examples/lin-ke/work/leafbox.md) | A wrong decision, written down, then reversed |
| [CHANGELOG.md](examples/lin-ke/shared/CHANGELOG.md) | Permission lives here. Git stores the diff |

Full week: [docs/walkthrough.md](docs/walkthrough.md) · or run `aimem tour`

![Monday write, Wednesday read, Sunday propose](assets/week.svg)

## The idea, three sentences

1. Long-term memory lives in **markdown you can open**, not in a vendor's hidden brain.
2. **Every AI reads the same folder.** Cursor, Claude, Codex, Grok — one notebook.
3. **An AI may propose. It does not write until you say so.** Wrong memory should not become "fact".

That is the whole invention. The CLI is optional.

## Why not "just let the AI remember"

Most memory tools ingest everything, embed it, and inject "relevant" chunks later. Convenient. Also how a wrong guess becomes next week's truth.

This method fails in a boring way: you forget to write a note.
Auto-memory fails in a dangerous way: it writes the wrong note, then defends it.

Vendor memory is fine for "what did we just talk about".
It is a bad unique source of truth across chats, tools, and weeks.

In the demo, Codex suggested "rewrite the README to get stars". Lin Ke rejected it. The rejection stays on the weekly list so the next scan cannot bring it back.

## Steal it without installing

Make a folder and save [MEMORY.en.md](https://hc-ui.github.io/cross-ai-memory/MEMORY.en.md) as `MEMORY.md`. Paste this into every AI. Replace `<VAULT>`.

```text
Long-term memory folder: <VAULT>
Entry: <VAULT>/MEMORY.md
Start at the entry. Then open only the notes the index names.
Do not read the whole folder.
Do not write a note unless I explicitly say:
记住 / remember / 同意写入 / approve write.
Propose the smallest change first.
Never store tokens, passwords, or cookies.
```

One topic, one note. Current user statements beat old notes. Verified facts beat guesses. If two notes disagree, say so — do not silently overwrite.

## Tonight, three steps

1. Make a local folder and save [MEMORY.en.md](https://hc-ui.github.io/cross-ai-memory/MEMORY.en.md) as `MEMORY.md`.
2. Copy the rule above and replace `<VAULT>` with that folder.
3. Paste it into Cursor / Claude / Codex.

When a durable fact should land, say `记住` or `approve write`. It should propose first. Short version: [docs/tonight.md](docs/tonight.md)

## Try the kit

```bash
pip install git+https://github.com/hc-ui/cross-ai-memory.git
aimem tour
aimem rule
aimem check examples/lin-ke
aimem init --demo ./look
```

![aimem check examples/lin-ke → 11 notes, ok](assets/check.svg)

`aimem init` copies an empty shell. `aimem init --demo` copies Lin Ke's notebook.

Point `<VAULT>` in `adapters/cursor.md` (or Claude / Codex) at that folder. Ask a question that needs last week's decision. The agent should open `MEMORY.md`, then one or two notes.

Say `记住` only when you want a note created.

- Commands and collector: [docs/cli.md](docs/cli.md)
- Rules that should not drift: [SPEC.md](SPEC.md)
- Questions: [docs/faq.md](docs/faq.md)

## What this is not

- Not a cloud memory API
- Not an embedding database
- Not a sync of ChatGPT / Claude / Cursor product memory
- Not a real person's notes — `examples/lin-ke` is a specimen

Local only. No API key. Do not publish a vault that contains your life.

## License

[MIT](LICENSE)

# FAQ

## Where do I start?

The page for strangers: [public site](https://hc-ui.github.io/cross-ai-memory/en.html). Docs map: [README.md](README.md). Specimen: [examples/lin-ke/MEMORY.md](../examples/lin-ke/MEMORY.md).

## Do I need the CLI?

No. The method is three rules and a folder of markdown. The CLI copies a starter, checks the folder, and reads local session files. You can steal the rules and never install anything.

## Do I need Obsidian?

No. Any editor is enough. Obsidian is convenient because `[[wikilinks]]` become clicks.

## Will this sync ChatGPT / Claude / Cursor product memory?

No. It only reads local session files you can already open on disk. Vendor hidden memory stays where it is.

## Is this Mem0 / claude-mem / a vector database?

No. Those tools ingest first and retrieve later. This kit writes last, and only after you approve. The source of truth is a note you can open.

## What if I use only one AI?

The notebook still beats a hidden product memory: you can search it, diff it, and take it to the next tool when you switch.

## Can the weekly job write notes by itself?

No. It prints a list. `aimem collect commit` only moves a local checkpoint. That is not `git commit` and not approval.

## I ended up with MEMORY.md.txt

Show file extensions, then delete `.txt`. In Notepad, Save As → UTF-8 → name `MEMORY.md`. Do not use Word.

## Should I publish my real vault?

No. Publish a method. Keep real notes private.

## Why reject "rewrite the README to get stars"?

Because that is a guess, not a durable fact. In the demo it is left on the proposal as a rejected item so the next scan does not bring it back.

# A week in the notebook

This is the same story as `aimem tour`. Every link is a real file.

Lin Ke is fictional. The week is the method.

## Monday · Cursor writes one fact

Lin Ke: new installers go to `E:/Apps`.

Cursor does not write yet. It proposes `CAND-20260824-01`.
Lin Ke says `同意写入`. Then Cursor creates:

[examples/lin-ke/shared/install-path.md](../examples/lin-ke/shared/install-path.md)

One topic. One note. One changelog row: `MEM-20260824-01`.

The raw Monday chat, as the collector would see it:

```bash
aimem collect normalize --source cursor --path examples/sessions/cursor-monday.jsonl
```

## Wednesday · Claude reads the same note

A new chat. A different product. Claude starts at [MEMORY.md](../examples/lin-ke/MEMORY.md), then the index, then the installer note.

It does not ask where files go.

That is the whole point of a shared notebook.

## Sunday · Codex only proposes

Codex scans the week's local sessions and writes a list. It still does not touch a canonical note.

Open [proposals/week-2026-08-24.md](../examples/lin-ke/proposals/week-2026-08-24.md).

| ID | Item | Result |
| --- | --- | --- |
| CAND-20260824-01 | installer path | approved and written |
| CAND-20260824-02 | rewrite README to get stars | rejected, do not list again |
| CAND-20260824-03 | leafbox man page tone | still open |

## The reversal

[work/leafbox.md](../examples/lin-ke/work/leafbox.md) first said "GBK on Windows". Two days later Lin Ke reversed it. The rejected idea stays on the page so the next chat cannot revive it.

Wrong memory that is written down can be reversed.
Wrong memory that lives in a vendor brain usually cannot.

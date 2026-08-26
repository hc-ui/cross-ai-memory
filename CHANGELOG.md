# Changelog

## 0.3.8 - 2026-08-26

- Vault check now shares secret detection with the collector redactor (JWT, Google API keys, AWS access keys) and reports unreadable notes instead of crashing.
- `scope: grok-heavy` is accepted, matching the collector source that already exists.
- Collector validates scan limits, rejects broken JSON config/state, ignores unreadable session trees, and cleans up failed atomic writes.
- `aimem init` copies adapter `.txt` paste blocks as well as `.md` files.
- CLI rejects non-positive collect limits and surfaces `OSError` / JSON errors as exit status 2.
- Tests cover health-check issue codes, collect read/commit/abandon, allowlist enforcement, and every session parser.
- Dev extra now includes Ruff. Updating `.github/workflows/ci.yml` needs a token with `workflow` scope.

## 0.3.7 - 2026-08-26

- Add a docs map and a Chinese CLI page, so the repo has one reading order.
- Drop the duplicate pictures under `site/assets/`. Pages copies from `assets/` only.

## 0.3.6 - 2026-08-26

- The public page now shows the specimen tree, the leafbox reversal, the permission ledger, the write gates, and a comparison with auto-memory.

## 0.3.5 - 2026-08-26

- Tonight now says how to save `MEMORY.md` on Windows, and ships a probe sentence that should open that file.
- The path box starts as `D:/my-memory`, so copying the rule never leaves a raw `<VAULT>`.

## 0.3.4 - 2026-08-26

- The public page fills `<VAULT>` from a path box, so the copied rule already has a folder.
- Step 3 names the paste target: Cursor user rules, Claude `CLAUDE.md`, Codex `AGENTS.md`.

## 0.3.3 - 2026-08-26

- Tonight on the public page is a folder plus MEMORY.md, not a CLI install.
- The paste rule now names `<VAULT>`, so “change the path” has a path to change.

## 0.3.2 - 2026-08-26

- Landing page wraps the title on a phone, leads with tonight’s three steps, and sends Chinese readers to the Chinese README.
- Demo vault and empty starter notes are Chinese-first, so a click from the public page does not drop into English.

## 0.3.1 - 2026-08-26

- Landing page now opens on a Wednesday chat contrast and the actual install-path note.
- Add a share line, Open Graph image, and favicon so a pasted link has a face.

## 0.3.0 - 2026-08-25

- Add a standalone story page for sharing: Chinese first, English second.
- Add `aimem rule` and a one-file paste block under `adapters/`.
- GitHub Pages publishes `site/`.

## 0.2.0 - 2026-08-25

- Add Lin Ke's lived-in demo vault, a week walkthrough, and a Sunday proposal list.
- Add `aimem tour` and `aimem init --demo`.
- Public page now leads with files a stranger can open, not with commands.

## 0.1.1 - 2026-08-25

- Public landing page now explains the idea to strangers first: three rules, a picture, then the install.
- Command and collector details moved to `docs/cli.md`.

## 0.1.0 - 2026-08-25

- First public kit: starter vault, Cursor / Claude / Codex adapters, `aimem` CLI.
- Collector ports the local allowlisted session scan used for weekly proposals.
- Health check covers frontmatter, wikilinks, expiry, reachability, and secret-like strings.

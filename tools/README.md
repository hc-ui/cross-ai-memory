# Tools

Windows 采集器和每周提示词。命令行版看 [docs/cli.zh-CN.md](../docs/cli.zh-CN.md)。

- `Collect-AIMemoryCandidates.ps1` is the original Windows collector. Defaults now use `%USERPROFILE%`. Same modes as `aimem collect`: Initialize, Scan, Read, Commit, Abandon, Status, Normalize.
- `weekly-proposal-prompt.md` is the full weekly job prompt. Replace `<VAULT>` and `<INBOX>` before pasting it into Codex or another scheduler.

The PowerShell `Commit` mode only advances the inbox checkpoint. It is not `git commit`.

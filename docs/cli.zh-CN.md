# 命令

已经懂方法、只要命令时看这页。刚进来先看 [README](../README.zh-CN.md) 或 [公开页](https://hc-ui.github.io/cross-ai-memory/)。

Python 3.10+，没有额外依赖。

```bash
pip install git+https://github.com/hc-ui/cross-ai-memory.git
aimem tour
aimem check examples/lin-ke
aimem init --demo ./look
aimem doctor ./look
```

| 命令 | 干什么 |
| --- | --- |
| `aimem tour` | 打印林可那一周 |
| `aimem rule` | 打印可粘贴规则（`--lang zh\|en`） |
| `aimem init [DIR]` | 复制空壳和 adapters |
| `aimem init --demo [DIR]` | 复制林可那本正在用的 |
| `aimem check [DIR]` | 只读检查 |
| `aimem doctor [DIR]` | 检查库，并列本机 AI 会话根目录 |
| `aimem collect init` | 把现有会话字节标成基线，不回填 |
| `aimem collect scan` | 列出新增或追加的允许文件 |
| `aimem collect read` | 收成用户/助手文本，遮蔽凭证 |
| `aimem collect commit` | 推进采集器检查点。不是 git 提交 |
| `aimem collect abandon` | 丢掉一次待处理扫描，不推进检查点 |
| `aimem collect status` | 显示 inbox 检查点和未提交扫描 |
| `aimem collect normalize` | 解析一个 jsonl，不动 inbox |

`collect` 不改正文。

Windows 也可以跑 `tools/Collect-AIMemoryCandidates.ps1`。同一套允许名单和检查点。

## 采集器读什么

只读本机会话，而且只取用户 / 助手正文：

| 来源 | 默认根目录 |
| --- | --- |
| Codex | `~/.codex/sessions`，`~/.codex/archived_sessions` |
| Claude Code | `~/.claude/projects` |
| Grok | `~/.grok/sessions` |
| Grok Heavy | `~/.grok-heavy/sessions` |
| Antigravity | `~/.gemini/antigravity/brain` |
| Cursor | `~/.cursor/projects`，以及 Cursor OD 聊天目录 |

系统提示、工具调用、工具结果、推理、鉴权、设置、缓存、附件、Codex 子代理线程都会跳过。文件静置 15 分钟后才会被扫到。来源轮流排队。

缺的根目录直接跳过。`aimem collect init` 之后，路径不对就改 `~/AI-Memory-Inbox/config.json`。

每周任务提示词：`tools/weekly-proposal-prompt.md`。

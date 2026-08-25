# cross-ai-memory

你已经同时用好几家 AI。它们各记各的，下场对话还是两眼一抹黑。

`cross-ai-memory` 是一套 **人工批准的本地长期记忆**。Markdown 才是唯一真相。AI 可以提案，你没点头它不能写。

[English](README.md) · [简体中文](README.zh-CN.md)

```text
本机会话文件  ->  只读采集  ->  每周拟更新清单
                                  |
                                  v
                           你批准某一条笔记
                                  |
                                  v
                           Obsidian / git 记忆库
```

## 这不是又一个记忆引擎

GitHub 上已经有很多自动灌库工具：把对话切碎、做向量、下次再“相关注入”。

这套反着做。

| | `cross-ai-memory` | 常见 Agent Memory |
| --- | --- | --- |
| 谁写库 | 你看过提案再写 | 模型自己持续写 |
| 真相在哪 | 能打开的笔记 | 向量库 / 图谱 |
| 跨 AI | 读多家本地会话文件 | 通常只服务一个产品 |
| 厂商隐藏记忆 | 不读、不同步 | 常常被当成事实 |
| 失败形态 | 漏记一条 | 静默记错 |

它更像归档纪律，不像 Mem0。

## 60 秒

Python 3.10+，零依赖。还没上 PyPI：

```bash
pip install git+https://github.com/hc-ui/cross-ai-memory.git
aimem init ./my-memory
aimem check ./my-memory
```

把 `my-memory/adapters/cursor.md`（或 Claude / Codex 那份）贴进对应 AI 的规则，把 `<VAULT>` 换成 `my-memory` 的路径。

问一个需要旧决定的问题。它应该先读 `MEMORY.md`，再读一两篇笔记，而不是把整个文件夹塞进上下文。

只有你想落笔记时再说 `记住` 或 `approve write`。

## 命令

| 命令 | 作用 |
| --- | --- |
| `aimem init [DIR]` | 复制启动库和适配器 |
| `aimem check [DIR]` | 只读健康检查 |
| `aimem doctor [DIR]` | 检查记忆库，并列出本机存在的 AI 会话目录 |
| `aimem collect init` | 把现有会话字节标成基线，不回填历史 |
| `aimem collect scan` | 列出新增或追加的允许清单文件 |
| `aimem collect read` | 只抽出 user/assistant 文本，并遮蔽疑似凭据 |
| `aimem collect commit` | 只推进采集检查点，不是 git commit |
| `aimem collect normalize` | 单独解析一份 jsonl，不动 inbox 状态 |

`collect` 不会改记忆库。

Windows 也可以用 `tools/Collect-AIMemoryCandidates.ps1`，允许清单和检查点语义与 Python 版相同。

## 采集器读什么

只读本机会话，而且只留 user / assistant 正文：

| 来源 | 默认目录 |
| --- | --- |
| Codex | `~/.codex/sessions`、`~/.codex/archived_sessions` |
| Claude Code | `~/.claude/projects` |
| Grok | `~/.grok/sessions` |
| Grok Heavy | `~/.grok-heavy/sessions` |
| Antigravity | `~/.gemini/antigravity/brain` |
| Cursor | `~/.cursor/projects` 以及 Cursor OD 的 chat 目录 |

系统提示、工具调用、工具结果、推理、鉴权文件、设置、缓存、附件、Codex 子代理会话一律跳过。文件要静置 15 分钟才会被扫到。来源之间公平轮询，不会让一家 AI 的积压占满整批。

本机没有的目录会跳过。路径不一样就在 `aimem collect init` 之后改 `~/AI-Memory-Inbox/config.json`。

## 批准口令

| 你说 | 可以 | 不可以 |
| --- | --- | --- |
| `同意写入` / `approve write` | 写指定笔记、`aimem check`、本地提交 | push |
| `同意推送` / `approve push` | 把已核验提交普通推送 | 强推 |
| `同意写入并推送` / `approve write and push` | 两段都做，检查失败就停 | 跳过检查 |

每周任务只该出清单。完整提示词在 `tools/weekly-proposal-prompt.md`。

## 隐私

- 只在本地运行。没有 API key，也没有云端记忆服务。
- inbox 只保存检查点，不保存完整原始对话。
- 常见 Token 会先被替换成 `[REDACTED]`。这不能证明所有秘密都找得到。
- 不要把真正的私人笔记发布到公开仓。本仓库只带示例库。

## License

[MIT](LICENSE)

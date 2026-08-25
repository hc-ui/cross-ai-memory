---
title: Memory governance
created: 2026-08-25
updated: 2026-08-25
last_confirmed: 2026-08-25
source: local_architecture
confidence: confirmed
status: active
scope: shared
note_type: canonical
tags:
  - ai-memory
  - governance
---

# 怎么读、怎么写

## 分层

| 层 | 存什么 | 不存什么 |
| --- | --- | --- |
| 厂商记忆 | 刚才那次对话的连贯 | 长期事实的唯一副本 |
| 共享笔记 | 每家 AI 都可能用到的事实 | 某一个工具的运行时碎屑 |
| 某家 AI 自己的笔记 | 只跟这个工具有关的证据 | 共享事实的复印件 |
| 会话文件 | 能打开的本地聊天原文 | 长期真相 |

这套工具只同步**你能打开的本地会话**。它不读厂商藏起来的记忆。

## 读

1. 自包含的工作不要进库。
2. 从 [[MEMORY]] 进，再看共享索引，再打开最少的几篇。
3. `updated` 只表示「文件改过」，不是「每一句今天都重新核过」。
4. 带 `review_after` 或 `confidence: confirmed_for_date` 的，过期要再核。

## 写

只有当前这句话明确批准，才写：

| 口令 | 允许 | 不允许 |
| --- | --- | --- |
| `同意写入` / `approve write` | 点名的笔记、`aimem check`、本地 git 提交 | 推送、上传云端 |
| `同意推送` / `approve push` | 已经检查过的普通推送 | 强制推送、加新远端 |
| `同意写入并推送` / `approve write and push` | 两件事都做；检查失败就停在推送前 | 跳过检查 |

做完一个普通任务不是批准。「以后也许有用」也不是批准。

## 字段

用入门模板。建议取值：

- `source`：`user_explicit`、`local_verified`、`official_source`、`session_summary`、`prior_memory`、`local_architecture`、`inference`（用 `_and_` 拼接）
- `confidence`：`confirmed`、`confirmed_for_date`、`mixed`、`unverified`
- `status`：`active`、`historical`、`deprecated`
- `note_type`：`index`、`canonical`、`snapshot`、`session`、`audit`、`readme`、`template`

正在用的快照必须有 `review_after`。超过 30 天的会话摘要，归档或折进正文。

## 冲突

- 偏好和自我描述：你现在说的 > 最近有来源的笔记 > 旧笔记 > 猜测
- 机器和外部事实：刚核过的 > 你说的 > 最近有来源的笔记 > 旧笔记 > 猜测
- 两边打架就两面都报。不许悄悄覆盖。

## 采集器

采集器只出提案清单。它的 `commit` 只推进一个用完即弃的本地检查点。那不是 git 提交，也不是改正文的批准。

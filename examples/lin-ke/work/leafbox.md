---
title: Lin Ke leafbox decisions
created: 2026-08-20
updated: 2026-08-22
last_confirmed: 2026-08-22
source: user_explicit_and_local_verified
confidence: mixed
status: active
scope: shared
note_type: canonical
tags:
  - demo
  - project
---

# leafbox

`leafbox` 是虚构的命令行：把目录树打成一份文本。不是真产品。

## 结论

标准输出用 UTF-8。不要输出 GBK。Windows 控制台乱码是控制台的事，不是改工具的理由。

## 证据

- 2026-08-20，Cursor，`同意写入`：第一版写过「Windows 用 GBK，演示好看」。
- 2026-08-22，Claude，`同意写入`：林可打开 `cmd.exe`，发现 GBK 版接到 Python 管道就断，改了回来。
- 还不确定：编码这件事没有。旧决定留在下面，免得下场 AI 再捡回来。

## 已经否过的

Windows 用 GBK。新对话再提，指到这里。林可没有新证据，就不要重开。

## 范围

只这一件虚构项目。安装路径仍在 [[shared/install-path]]。

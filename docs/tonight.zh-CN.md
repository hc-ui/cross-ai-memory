# 今晚就能抄走

不用装命令行，也不用把整个仓库读完。

1. 建一个本地文件夹，把 [MEMORY.md](https://hc-ui.github.io/cross-ai-memory/MEMORY.md) 存进去。
2. 在 [公开页](https://hc-ui.github.io/cross-ai-memory/) 填入这个路径，复制已经填好的规则。
3. 同一段贴三处：Cursor 用户规则、Claude 的 `CLAUDE.md`、Codex 的 `AGENTS.md`。

下次要落一条长期事实，说「记住」或「同意写入」。它应该先提案，你点头再写。

想要完整空壳或林可那本，再装：

```bash
pip install git+https://github.com/hc-ui/cross-ai-memory.git
aimem init ./my-memory
aimem init --demo ./look
```

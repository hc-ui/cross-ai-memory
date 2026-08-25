# 今晚就能抄走

不用装命令行，也不用把整个仓库读完。

1. 建一个本地文件夹，把 [MEMORY.md](https://hc-ui.github.io/cross-ai-memory/MEMORY.md) 存进去。
2. 复制公开页上的规则，把 `<VAULT>` 换成这个文件夹。
3. 贴进 Cursor / Claude / Codex。

下次要落一条长期事实，说「记住」或「同意写入」。它应该先提案，你点头再写。

想要完整空壳或林可那本，再装：

```bash
pip install git+https://github.com/hc-ui/cross-ai-memory.git
aimem init ./my-memory
aimem init --demo ./look
```

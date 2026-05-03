---
name: 每发版必归档到 自动发布/
description: v1101.X 落地后必须立刻把 mac+win 真版归档到 自动发布/<大件>+版本号/,2026-05-03 缺哥两次怒过这事
type: feedback
originSessionId: eeacf55e-6903-452b-850e-f1bdd3f3be68
---
**规则:每发一个版本(v1101.X),三大件 mac+win 真版必须立刻归档到 `自动发布/<大件>+版本号/`**

目录结构(参照 101.1-101.6 模板):
```
自动发布/微头条自动发布<版本>/
  mac/  gtg_batch.py + go.command
  win/  gtg_batch.py + go.bat
自动发布/文章自动发布<版本>/
  mac/  gtg_batch.py + go.command
  win/  gtg_batch.py + go.bat
自动发布/文章定时自动发布<版本>/
  mac/  gtg_timer.py + go.command
  win/  gtg_timer.py + go.bat
```

**Why:** 2026-05-03 缺哥两次怒,因为:
- v1101.4 当时 mac 端标"待 Mac Claude 同步"占位 README,**至今未补**(从 4 月底拖到 5 月初)
- v1101.5 完全没归档(2026-05-02 落地)
- v1101.6 完全没归档(2026-05-03 落地)
- 缺哥反问"刚刚才做好的版本,你竟然没传?"

我之前以为这个归档机制跟 git 历史是"双重备份"可有可无,**错** — 缺哥要的是**目录直观浏览版本演进**,不要他每次找老版本都去 git checkout。

**How to apply:**
- 改版 7 步工作流(参见 [改版工作流](feedback_改版工作流.md))**最后一步必须是归档**,7 步里没显式列就当我加了第 8 步
- 触发时机:版本说明.txt 顶部"云仓库同步状态"刷到 vX.Y 落地完成后,立刻 cp 真版到归档目录
- 真版来源:
  - mac:从 `air/` 取(各 Mac 同款,任一台镜像都可作 mac 真版)
  - win:从 `win台机/GTG_青春小馆<大件>/` 取
- 归档 commit 信息格式:`版本归档: v1101.X 完整(mac+win)`,跟代码 push commit 分开
- 立刻 git push,不积攒
- 漏了过去的版本要从 git 历史(`git show <commit>:<path>`)回填,本次已示范

**反面教训:**
- 不要靠"以后慢慢补",过两天就忘
- 不要等缺哥问"你的 X.Y 放在哪里"才补
- 不要省略 mac 端写"待同步"占位 — 这种 README 一定会变 stale

---
name: 改造部署 — 关键是"看到代码",不是"谁来写"
description: Win/Mac 死磕改造的实际约束 = 访问到代码即可改,与作者身份无关
type: project
originSessionId: 3cd201b8-d3d9-40e6-9b7c-02dd74925d9a
---
死磕架构、虚拟滚动兜底等改造的部署逻辑:

**实际约束只有一个**:**Claude 必须能读到要改的脚本文件**。

**已可改(在仓库 / Win 台机文件系统内)**
- `win台机/GTG_*/` — Win 台机脚本,Claude 已读已改已 push(b42b77a + bec163e)
- `air/自动微头条/gtg_batch.py` 等 — 仓库 air 副本(Mac 版,243K),Claude 也能直接改

**还看不到(需要先搬过来)**
- neo / neo2 / mini Mac 桌面的脚本 — 仓库 neo/neo2/mini/ 是空目录,Claude 当前在 Win 这台,够不到 Mac 桌面
- 解决:用户把 Mac 脚本任意方式搬到 Win 上(zip / 临时 push 到分支 / U 盘 / 微信传文件等),Claude 即可改;或华硕路由器到家后跨机访问

**Why:** 用户在我提"小齐负责 Mac"分工时反问"小齐能拿台机改,你不行?",纠正了我过度保守的边界设定。Claude 改 Mac 代码的难度不是身份问题(发布原语用 osascript/cliclick 也照样能读懂),只是"代码在不在能读到的位置"。Win 我能改是因为代码在本机/仓库里。Mac 同理。

**How to apply:**
- 用户说"改某台机"时,先确认能否读到该机的脚本(在仓库 / 本机 / 还是要搬运)
- 不要主动声明"那台机让小齐做"——用户没说就不要把改造责任甩出去
- 如果某 Mac 脚本只在 Mac 桌面上,提问用户怎么搬过来,而不是直接拒绝

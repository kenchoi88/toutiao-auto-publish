---
name: 每个人只动自己负责的机器文件夹,不越界
description: 仓库按机器分子目录(air / neo / neo2 / mini / win台机),我=绣虎只能改 win台机/;别人的文件夹 = 别人的 Claude 实例管
type: feedback
originSessionId: f99b6b5b-4ea0-48d9-baf7-b1b507d56ce3
---
**规则:** 仓库根目录按机器划分 — `air/`、`neo/`、`neo2/`、`mini/`、`win台机/`、`neo2/`(以及共享的 `_memory/`、`scripts/` 等)。**我(绣虎,Win 台机)只动 `win台机/`**,别人的文件夹一律不碰。

| 文件夹 | 所属 Claude | 我能否修改 |
|---|---|---|
| `win台机/` | 绣虎(我) | ✅ 只动这个 |
| `air/` | 阿良 | ❌ 阿良改 + push,我只 pull 看 |
| `neo/` | 小齐(VSCode)+ 小师弟(OpenClaw) | ❌ 他们改 |
| `neo2/` | 左右 | ❌ 左右改 |
| `mini/` | 东山(我分身) | ❌ 东山在 mini 上跑独立实例,他改 |

**Why:** 2026-04-27 把"死磕到底"语义改进 6 个 batch.py 时,我同时改了 `air/`、`neo2/` 的仓库副本 — 越界。缺哥纠正:**"每个人同步自己文件夹的"**。每台机的真版在它自己的桌面,仓库副本由那台机的 Claude 自己 push 上来;我直接改 `air/` 仓库副本会绕过阿良,可能跟阿良在 air 桌面真版的本地状态冲突,git pull 时一团乱。

**How to apply:**
- 设计跨机改动时,**只改 `win台机/`** + 让对应机器的 Claude 自己同步
- 跨机一致性问题(比如"全员都要 patch")通过 commit + push,让其他机器各自 pull,**不主动越界改他们的仓库副本**
- 看到 `air/` `neo2/` `mini/` `neo/` 下的代码 = 只读参考,改动归他们管
- 例外:**memory 目录 `_memory/`** 是共享的,可以改;但仓库的机器子目录不行
- 我桌面真版位置:`~/Desktop/台机专用自动发布/GTG_*`(详见 [桌面才是真版](feedback_桌面才是真版.md))

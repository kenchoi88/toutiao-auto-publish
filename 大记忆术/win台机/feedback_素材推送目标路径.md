---
name: 素材推送 = 大件子目录 / 素材,不是顶级别名目录
description: 微头条 / 文章 / 文章定时素材推送的正确目标都是 ~/Desktop/<大件名>/素材/,不是顶级历史别名(自动微头条素材/ 等);代码 BASE_DIR + "素材" 只读子目录
type: feedback
originSessionId: 231b8291-86e8-48aa-b91b-26f7b22ff45c
---
各 Mac 上各大件的素材池正确路径都是 `~/Desktop/<大件名>/素材/`(大件目录下的子目录),**不要**推到顶级的别名目录(如 `~/Desktop/自动微头条素材/`)。

| 大件 | 正确推送目标 |
|---|---|
| 微头条 | `~/Desktop/微头条自动发布/素材/` |
| 文章自动 | `~/Desktop/文章自动发布/素材/` |
| 文章定时 | `~/Desktop/文章定时自动发布/素材/` (neo2 是 symlink → `~/code/.../Mac文章定时自动发布/素材/`) |

**Why:** gtg_batch.py / gtg_timer.py 里 `DOCS_FOLDER = os.path.join(BASE_DIR, "素材")`,BASE_DIR = 大件目录。代码只读子目录;顶级 `~/Desktop/自动微头条素材/` 是历史遗留别名,gtg_batch 完全不读。2026-04-30 凌晨我误把 mini/neo2/neo 的 wtt 全推到了顶级 `~/Desktop/自动微头条素材/`,缺哥发现后让我 mv 到大件子目录,纠正。

**How to apply:**
1. 推素材到 mac 任何一台时,目标永远是 `~/Desktop/<大件名>/素材/`,不要选顶级别名目录,即便那个目录存在。
2. 推前先 `grep -nE "DOCS_FOLDER|SOURCE" 大件/gtg_*.py` 确认代码读的真实路径,别凭直觉选目录。
3. 顶级 `~/Desktop/自动微头条素材/` 这种别名目录见到也别用,可能是历史遗留;留空别删(用户可能日后整理)。

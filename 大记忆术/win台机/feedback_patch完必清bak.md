---
name: patch 完必清 .bak / 临时监听用完即删
description: patch/clear/align/drop 验证后必清该轮 .bak + __pycache__ + ~$*;临时 hook / 监听 / cron 同样用完即拆,不囤积
type: feedback
originSessionId: b5e5a8ce-2387-44d4-9851-658903ac1976
---
每次 patch / clear / align / drop / sheet 改动完成且验证通过(改版 7 步末)→ 立刻清该轮 .bak 和 __pycache__ / ~$*.xlsx / .DS_Store 等散文件,不积累。

**临时监听同款:** 为某次清场临时加的 hook(settings.json)、监听器(fswatch / 守护进程)、定时任务(cron / launchd / 计划任务)、临时 patch 脚本 — 任务完成立刻拆,不留作"以后可能用得上"。需要长期保留的工具放 `自动发布/工具/` 并 commit;不入仓库的就该删。

**Why:** 2026-05-05 缺哥怒「以前都没这么多东西,越来越多」。实测 Win 台机三大件累计 .bak 57 个(微头条 17 / 文章 23 / 文章定时 17),NEO2 67 个,根因是每次 patch 留 .bak 不主动清。.bak 当"落地证据"是 v1101.3 那批的临时用法,核完就该删 — git 仓库 + 自动发布V1102.2/ 归档已是权威证据,本地 .bak 长期保留是冗余,文件夹只会越来越乱。

**How to apply:**
1. 改桌面真版前 cp .bak(临时保险,允许)
2. 跑完验证 + 同步仓库 + 全机落地后(改版 7 步末)→ 立刻 `rm <件目录>/*.bak_* *.bak.* -r __pycache__ '~$'*.xlsx .DS_Store`
3. 跨机 patch / clear / align / drop:目标机执行 + 验证 idempotent 通过后,立刻 ssh 进去删本机这一轮的 .bak
4. xlsx_align.py 已内置 idempotent 自清(无改动自动删备份);clear / drop / sheet 改动类工具应同样自清
5. 当天的 .bak 也清 — 不再当"落地证据",改用 git log + grep patch 标记 + md5 验证(详见 feedback_声明前先实证 / feedback_推版本必须全验证再汇报)
6. 跨机扫一遍同款命令:`ssh <user>@<ip> "rm -f ~/Desktop/*/*.bak_* ~/Desktop/*/*.bak.* -rf ~/Desktop/*/__pycache__"`,纳入"改版 7 步"完成后的标准动作

---
name: v1101 spec(本地副本,真版在仓库 shared_memory/project_v1101_spec.md)
description: 三大件 v1101 基线;改前先读仓库版,这条只是索引
type: project
originSessionId: ff29c897-007d-4a45-9b62-72d88385b0eb
---
真版:`c:\Users\kench\code\头条自动发布\shared_memory\project_v1101_spec.md`(已 commit + push)

10 个 patches:
- P1 删 Step 3 6s
- P2 字数<50 重试
- P3 ProseMirror 取最长
- P4 [DIAG] 确认发布(不含微头条)
- P5 ensure_gtg_top 强化(unhide+AXRaise+verify+重试)
- P6 Win 飘屏外坐标兜底(只 win)
- P7 cliclick 重试(2-3 次再判失败)
- P8 抄 win 8 处搜索框(只 mac 文章定时)
- P9 抄 win 阅读量回查(只 mac 文章定时)
- P10 Stage 2 死磕加熔断(只 文章定时)

每脚本完成度核对表见仓库版。

**Why:** 缺哥 2026-04-28 拍 — 不再补漏式,以 v1101 为统一基线,完成度核对表全 ✅ 才算完。

**How to apply:** 改前 grep 仓库 spec,改完逐项核对。

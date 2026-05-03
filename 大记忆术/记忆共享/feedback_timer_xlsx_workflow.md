---
name: 定时发布xlsx改时间的工作流
description: 每次跑定时发布前，缺哥会主动找我改xlsx时间，不要自动化或提前分发
type: feedback
originSessionId: 6d63652c-70fe-4a61-b1a1-aedeb12cf6ad
---
每次定时发布前，缺哥会让阿良介入改 `定时发布.xlsx` 里的发布时间，不需要主动操心xlsx分发。

**Why:** `*.xlsx` 在 .gitignore 里，4台机器各自本地维护。缺哥喜欢人在场看着改，而不是搞自动化分发——节奏由他控。

**How to apply:**
- 不要主动写脚本/cron来同步分发 xlsx
- 不要在改完Air后主动追问"其他机器怎么办"
- 等缺哥说"要跑定时发布了"再行动，按他的节奏一台一台改
- 现成可用：缺哥的5台机器里 Air/neo/mini/台机/neo2，要改时通过SSH或Tailscale接入即可

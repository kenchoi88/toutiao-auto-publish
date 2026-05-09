---
name: 罐头数据膨胀 ≈ 登录账号数
description: 罐头资源库占用主要来自每个登录账号的浏览器缓存,账号多则膨胀大,NEO2 73G/MINI 89G/NEO 96G
type: reference
originSessionId: 65e7943b-4b50-4d8f-8d15-a85ca3997cff
---
罐头本地数据(~/Library/Application Support/创作罐头/)膨胀主要来自每个登录发文账号的浏览器缓存/cookie/localStorage/IndexedDB(罐头基于 Electron/Chromium,每个账号 session 独立存储),账号越多越大。

实证 2026-05-09 三机对比:
- NEO 96G(账号最多)
- MINI 89G
- NEO2 73G(账号少 → 缓存少 → 最瘦)

应用:
- 看到罐头数据异常膨胀先核账号数,账号多属正常,不必强清
- 罐头数据是业务核心(含登录态/cookie/草稿/发文历史),清错可能丢账号登录,慎清
- 跨机磁盘对比时,罐头部分要按账号数归一化,不能直接比绝对值

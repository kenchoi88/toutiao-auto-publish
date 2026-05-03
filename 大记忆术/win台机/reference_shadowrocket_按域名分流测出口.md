---
name: Shadowrocket 按域名分流测出口(本地副本)
description: ipinfo.io 出口 ≠ toutiao 出口;判头条是否走代理用 TLS RTT 不要凭 ipinfo / route get
type: reference
originSessionId: 6198d8da-e501-4a0b-b8de-45446700703e
---
真版在 `c:\Users\kench\code\头条自动发布\shared_memory\reference_shadowrocket_按域名分流测出口.md`。

**核心**:Shadowrocket TUN 按域名规则分流,**不同域名走不同出口**。
- ipinfo.io = 国外服务通常走代理 → 出口 LA / 东京
- mp.toutiao.com = 国内 DIRECT 规则 → 出口国内电信
两者**不能互推**。

**铁证 = TLS RTT**:
- 国内直连 50-110ms
- 国外代理 1000ms+
- 差一个数量级,闭眼分辨

**不可信**:`route get`(Shadowrocket TUN 一律 utun9)/ `nslookup`(fake-DNS 198.18.x)。

**Why:** 2026-05-02 我用 ipinfo 判头条流量走代理,推 air reboot,结果阿良 TLS RTT 实测头条 50-75ms 跟百度同档 = **国内直连,我误判**。

**How to apply:**
- 任何"是否走代理"问题 — 第一动作 TLS RTT 不是 ipinfo
- 跨域名出口结论是错的,Shadowrocket 分流不同域名不同出口
- 写 patch / 改 db / 让用户 reboot 之前先 TLS RTT 验证

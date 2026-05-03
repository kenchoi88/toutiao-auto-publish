---
name: 4 台 Mac Shadowrocket 必须 bypass Tailscale 100.64.0.0/10
description: Shadowrocket 接管全 TCP 流量,Tailscale CGNAT 段(100.x.x.x)若不放行,跨机 SSH/HTTP 全挂(ICMP 不走代理仍通,易误判)
type: reference
originSessionId: f99b6b5b-4ea0-48d9-baf7-b1b507d56ce3
---
**问题:** 4 台 Mac(air / mini / neo / neo2)都装了 Shadowrocket。Shadowrocket 默认接管系统 TCP 流量,Tailscale 用的 **CGNAT 段 `100.64.0.0/10`**(包括所有 100.x.x.x peer IP)如果没在 bypass 规则里 → 跨机 SSH / HTTP / 任何 TCP 流量被代理拦,看起来"100.x ping 通(ICMP)但 SSH 不通"。

**实测(2026-04-27):**

| Mac | Shadowrocket 状态 | Tailscale 100.x TCP/22 |
|---|---|---|
| neo2 | 关 | ✅ 通 |
| air / mini / neo | 开 | ❌ 全拦 |

**修复(每台 Mac 各配一次):**
1. 打开 Shadowrocket
2. 设置 / 路由 / 旁路规则 加:
   - `IP-CIDR,100.64.0.0/10,DIRECT`(Tailscale CGNAT 全段)
3. 保存,重启 Shadowrocket(让规则生效)

**Why:** Shadowrocket 跟 v2rayN(Win 台机)同类问题,但走 NetworkExtension 不走系统代理,所以 Win 那套 ProxyOverride 思路没法直接搬。各机各自配。

**How to apply:**
- 看到"Tailscale 节点显示在线但 SSH/HTTP 走 100.x 不通" — 先想火箭/clash 类代理是否拦了 100.x
- ICMP 通 ≠ TCP 通(代理常常只接管 TCP),诊断不要止步于 ping
- neo2 是参考样本(没开火箭的对照组,跨机功能正常)
- 此 bypass 配完前,跨机功能(SSH/SMB/同步)只能通过局域网 IP(192.168.50.x),不能用 Tailscale 100.x

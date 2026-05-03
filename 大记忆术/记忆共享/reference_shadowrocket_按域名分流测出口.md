---
name: Shadowrocket 按域名分流 — 测特定域名出口要看 TLS RTT 不能凭 ipinfo
description: Shadowrocket TUN 模式按域名规则分流,ipinfo.io 出口跟 toutiao.com 出口可能完全不同;判某域名是否走代理用 TLS RTT 或域名 traceroute
type: reference
scope: 4 Mac (air/neo/neo2/mini) + Win 台机
effective: 2026-05-02
---

> **2026-05-02 阿良教训** — 我(绣虎)用 ipinfo.io 出口判断头条流量是否走代理,**错了**。
> Shadowrocket 按域名规则分流,**不同域名走不同出口**。

## 错误方法论(不能再用)

```
ipinfo.io 出口 = ??? 国
→ 推断 → 该机所有流量都走这个出口
→ 推断 → 头条流量也走代理 (X 错!)
```

**ipinfo.io 是国外服务**,Shadowrocket 通常把它列为 PROXY → 走代理(美国/日本节点)。
**mp.toutiao.com 在国内 DIRECT 列表** → 走 en0 直连国内。

两者出口不一样,不能等价。

## 正确方法 — TLS RTT(铁证,剔除 fake-IP 误判)

```bash
# 测某域名是否走代理:看 TLS 握手 RTT
curl -o /dev/null -s -w '%{time_appconnect}\n' --max-time 8 https://mp.toutiao.com
```

判读标准(2026-05-02 实测):
| 出口 | TLS RTT |
|---|---|
| **国内直连**(电信→国内机房)| **50-110ms**(头条/百度/腾讯/淘宝同档)|
| **国外代理**(电信→美国节点→国外服务)| **1000ms+**(google/github)|
| 国外代理 → 回国内服务 | **300ms+**(明显比直连慢)|

差一个数量级 — 闭眼能分辨。

## 看出口的几种方法,各自适用场景

| 方法 | 适用 | 误判风险 |
|------|---|---|
| `route get <domain>` | **不可信** | Shadowrocket TUN 一律返 utun9(fake-IP 段),看不出真实出口 |
| `curl ipinfo.io` | 看那一域名的出口 | **不能反推其他域名** |
| `nslookup` / `dig` | 看 DNS 解析 | Shadowrocket fake-DNS 返 198.18.x — 看不出真实 IP |
| **TLS RTT** | **任何域名,铁证** | ✓ 推荐 |
| `myip.ipip.net` | ipip.net 在 DIRECT 时返电信 IP | 仅证 ipip.net 走 DIRECT,不证 toutiao |
| 抓包看真实远端 IP | 终极手段 | 复杂 |

## 判头条流量是否走代理 — 标准 3 步

```bash
# 1. 头条系 TLS RTT
curl -o /dev/null -s -w 'mp.toutiao.com TLS: %{time_appconnect}s\n' --max-time 8 https://mp.toutiao.com

# 2. 国内对照
curl -o /dev/null -s -w 'baidu.com TLS:      %{time_appconnect}s\n' --max-time 8 https://www.baidu.com

# 3. 国外对照(代理表现)
curl -o /dev/null -s -w 'google.com TLS:     %{time_appconnect}s\n' --max-time 8 https://www.google.com
```

判读:
- 头条系跟百度同档(50-110ms)→ ✓ 头条走 DIRECT 国内直连
- 头条系跟 google 同档(1000ms+)→ ✗ 头条走代理(配置错)

## How to apply

- 任何"流量是否走代理"问题 — **第一动作 TLS RTT 测试**,不要凭 ipinfo / route get
- 跨域名出口结论(A 走代理 → B 也走代理)是错的,Shadowrocket 按规则分流
- 写 patch / 改 db 之前先做 TLS RTT 测试,**有问题再修,不要瞎改**

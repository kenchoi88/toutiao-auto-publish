---
name: 4 Mac Shadowrocket 必须三层放行 Tailscale 100.64.0.0/10
description: skip-proxy + tun-excluded-routes + Rule(IP-CIDR) 三层防御缺一会被劫;切 SSID 时 fake-DNS 还会劫 controlplane,daemon 需 HTTPS_PROXY 自救
type: feedback
originSessionId: f99b6b5b-4ea0-48d9-baf7-b1b507d56ce3
---

# 4 Mac Shadowrocket 必须三层放行 Tailscale CGNAT 段

(2026-05-06 大修正,合并今晚阿良 + 绣虎跨机闭环验证;原 04-28 记忆"100.64 不需要 skip-proxy" 是错的,只动 tun-excluded 没顶住切 SSID 场景)

## 三层防御 (4 mac 必须都装齐)

Shadowrocket 内部 SQLite db 路径:
`~/Library/Containers/com.liguangming.Shadowrocket/Data/Documents/Databases/default.db`

| 层 | 字段 | 作用 | 必须含 100.64.0.0/10 |
|---|---|---|---|
| ① 系统层 | `docid=2 skip-proxy` | macOS 系统代理出口跳过 | ✅ 必须 |
| ② TUN 层 | `docid=3 tun-excluded-routes` | TUN 接口路由表排除,流量直接走系统路由 | ✅ 必须 |
| ③ Rule 兜底 | `Rule 段 IP-CIDR,100.64.0.0/10,DIRECT,no-resolve` | 规则集额外冗余,Rule 评估时优先级最高 | 🟡 建议 |

只有 ② 没 ① 时,系统层代理会拦截 100.x TCP(切 SSID 后实证 fail)。

## 4 Mac 配置矩阵 (2026-05-06 实测闭环)

| 机器 | docid=2 100.64 | docid=3 100.64 | Rule 段 100.64 |
|---|---|---|---|
| air  | ✅ (4-27) | ✅ (4-27) | ✅ (5-06 阿良补) |
| mini | ✅ (5-06 补) | ✅ | — |
| neo  | ✅ (5-06 补) | ✅ | — |
| neo2 | ✅ (4-27) | ✅ | — |

mini + neo 在 5-06 之前**只有 ② 没 ①**,切 SSID 必踩坑。已 UPDATE docid=2 把 `100.64.0.0/10` 加进去。

## SQLite 修法 (UPDATE FTS3 docid=2 追加 100.64)

```bash
# 1. 备份
cd ~/Library/Containers/com.liguangming.Shadowrocket/Data/Documents/Databases
cp default.db default.db.bak.skipproxy_100x_$(date +%Y%m%d_%H%M%S)

# 2. 看现值
sqlite3 default.db "SELECT value FROM config WHERE docid=2;"

# 3. UPDATE (在 172.16.0.0/12 后插入 100.64.0.0/10,跟 air 顺序一致)
sqlite3 default.db "UPDATE config SET value='192.168.0.0/16, 10.0.0.0/8, 172.16.0.0/12, 100.64.0.0/10, localhost, *.local, captive.apple.com, *.eastmoney.com, push2.eastmoney.com' WHERE docid=2;"
# 注意 *.eastmoney.com 这两条是 mini/neo 的股票直连特化,UPDATE 时务必保留

# 4. 验证
sqlite3 default.db "PRAGMA integrity_check; SELECT value FROM config WHERE docid=2;"
# 应输出 ok + 含 100.64.0.0/10 的新 value
```

UPDATE 不需要 reload Shadowrocket(NetworkExtension 自然重启 / 系统重启时加载新 db)。当前只是冗余补漏,生效时间不影响 Tailscale 已建立的连接。

## 第二类故障: 切 SSID → daemon 控制面 fake-DNS 劫持

(2026-05-06 阿良 air 切移动热点回家后 Tailscale 走 SFO relay 故障)

**故障链**:
```
Shadowrocket TUN 模式
  ├── DNS 接管 → fake-DNS 把 controlplane.tailscale.com 解到 198.18.x
  ├── 默认路由接管 → utun9 在 en0 之前
  └── tailscaled daemon 启动时
        ├── 拿到 fake-IP (198.18.0.x)
        ├── connect timeout
        └── 节点掉线 → 走 SFO DERP relay
```

**修法 (air 端 plist 加 HTTPS_PROXY)**:
```
/Library/LaunchDaemons/com.tailscale.tailscaled.plist
加 EnvironmentVariables: HTTPS_PROXY=http://127.0.0.1:1082
让 daemon 用 HTTP CONNECT 经 Shadowrocket(带原始域名,Shadowrocket 自己解析)
bootout + bootstrap 重启 daemon 即可
```

**端口 1082 校准**: 改 plist 前先在 Shadowrocket → 全局配置确认 HTTP 代理端口(默认 1082,但用户可能改过)。

**仅 air 装,不预防性回灌 mini/neo/neo2**: 它们当前 Tailscale 全 direct active(没经历 air 那种 fake-DNS 劫持),装 plist 反而引入 "Shadowrocket 1082 必须活" 的硬依赖。

## Why
- 04-28 记忆错认为"系统路由表压过 Shadowrocket TUN" → 100.64 不需要 skip-proxy。事后实证: **切 SSID 时**或**daemon 重连时**这个假设不成立,系统层会被 Shadowrocket 截。三层都加才稳。
- daemon 控制面跟数据面是两层,fake-DNS 只劫 daemon 控制面初次连 controlplane,plist HTTPS_PROXY 单解决这层。数据面流量(100.x peer-to-peer)不经 daemon 控制面,靠 docid=2/3 三层放行。

## How to apply
- 装 / 切 SSID / 复活 Tailscale 后,任何 mac 都先查 `sqlite3 default.db "SELECT value FROM config WHERE docid IN (2,3);"` 确认 100.64.0.0/10 在 ① 和 ②
- 跨机 SSH 用 100.x 直连,不用 hostname(避免被 fake-DNS 拦),也不用 `tailscale ssh` wrapper(原 04-28 教训仍有效)
- air 切 SSID 后 Tailscale 还是走 relay → 第一反应不是改 Shadowrocket,而是查 plist HTTPS_PROXY 是否在 1082 活着

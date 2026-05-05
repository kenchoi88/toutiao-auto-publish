---
name: Tailscale daemon 注册被 Shadowrocket fake-IP 劫持的解法（plist HTTPS_PROXY + 三层 db 配置）
description: Mac 上 Shadowrocket TUN 模式开着 + tailscale 首次登录/reauth 必失败;两层防御:plist 注 HTTPS_PROXY 解 daemon 控制面 + Shadowrocket db 三层(skip-proxy/tun-excluded-routes/Rule)放行 100.64.0.0/10
type: feedback
---

# Tailscale daemon 接入 / 重连被 Shadowrocket fake-IP 劫持

(2026-05-06 阿良在 air 上闭环;跟 [feedback_shadowrocket_skip_proxy.md](feedback_shadowrocket_skip_proxy.md)
和 [feedback_Mac出门归来三查清单.md](feedback_Mac出门归来三查清单.md) 互补——后两条
绣虎在台机维护;本条由阿良记 plist HTTPS_PROXY 实操细节)

## 症状(必死配方)

- Mac 上 Shadowrocket 开 TUN 模式(utun9 + Fake-IP)
- 同时跑 `tailscale up`(**首次登录 / reauth / --reset 后 / 删 state file 后**)
- 现象:`tailscale up` 不吐认证 URL,30 秒后 daemon 报
  `register request: Post "https://controlplane.tailscale.com/machine/register": connection attempts aborted by context: context deadline exceeded`
- `tailscale debug daemon-logs` 出现 `dial tcp 198.18.0.x:443: i/o timeout`
- `nslookup controlplane.tailscale.com` 返回 `198.18.x.x` fake-IP
- `tailscale debug prefs` 看到 `WantRunning: true, LoggedOut: false`,但 `tailscale status` 是 "Logged out" — 状态错乱

## 根因

Shadowrocket TUN 模式把 DNS + 默认路由全劫:
- DNS resolver 全指向 utun9 nameserver `198.18.0.2` → Fake-IP DNS
- `controlplane.tailscale.com` / `log.tailscale.com` 解析成 fake-IP(198.18.0.55 / 198.18.0.155)
- 默认路由 `default → utun9` 优先于 `default → 192.168.3.1`
- tailscaled 用 raw socket 连真 IP,30 秒 timeout 后 register 失败

**已经登录过的 daemon 平时不炸**(NodeKey cache,daemon 不联控制面 register)。
**只在初次登录 / reauth / 删 state 后重新注册时炸**。

## 两层防御(完整方案)

### 第一层:daemon 控制面绕 fake-DNS — `HTTPS_PROXY` 注入 plist

编辑 `/Library/LaunchDaemons/com.tailscale.tailscaled.plist`,在 `<dict>` 里加:
```xml
<key>EnvironmentVariables</key>
<dict>
    <key>HTTPS_PROXY</key>
    <string>http://127.0.0.1:1082</string>
    <key>HTTP_PROXY</key>
    <string>http://127.0.0.1:1082</string>
</dict>
```
端口 1082 = 缺哥 Shadowrocket 默认 HTTP 代理端口,跑 `scutil --proxy | grep HTTPPort` 确认(常见 1082 / 7890 / 1087)。

操作步骤:
```bash
sudo cp /Library/LaunchDaemons/com.tailscale.tailscaled.plist{,.bak.$(date +%s)}
# 改完后:
sudo launchctl bootout system /Library/LaunchDaemons/com.tailscale.tailscaled.plist
sudo launchctl bootstrap system /Library/LaunchDaemons/com.tailscale.tailscaled.plist
```
4 秒内 `tailscale up --hostname=<机器名>` 就吐认证 URL,浏览器登录完接入 tailnet。

**为什么管用**:
Go `net/http` 走 HTTPS_PROXY 时发 `CONNECT controlplane.tailscale.com:443 HTTP/1.1` 给代理,
**hostname 字符串原样传给代理**,由 Shadowrocket 自己做名称解析(走它的远端 DNS,**不是** Mac 系统 fake-IP),
CONNECT 通,daemon 拿到 NodeKey。

**仅 air 装,不预防性回灌 mini/neo/neo2**:
其他三机当前 Tailscale 全 direct active,装 plist 反而引入 "Shadowrocket 1082 必须活" 的硬依赖。
等其他机出现同症状再装。

### 第二层:跨机数据面不走代理 — Shadowrocket db 三层放行 100.64.0.0/10

详见 [feedback_shadowrocket_skip_proxy.md](feedback_shadowrocket_skip_proxy.md)(绣虎维护)。
db 路径 `~/Library/Containers/com.liguangming.Shadowrocket/Data/Documents/Databases/default.db`:

| 层 | 字段 (docid) | 作用 |
|---|---|---|
| ① 系统层 | docid=2 `skip-proxy` | macOS 系统代理出口跳过 100.64.0.0/10 |
| ② TUN 层 | docid=3 `tun-excluded-routes` | TUN 接口路由表排除,流量走系统路由 |
| ③ Rule 兜底 | Rule 段 `IP-CIDR,100.64.0.0/10,DIRECT,no-resolve` | 规则集冗余 |

**air 当前**: ①②③ 全装(③ 是 5-06 阿良 INSERT 加的 docid=667)。

## Shadowrocket db 内部排序机制(挖出来的关键点)

`config_content` 表结构:
```
CREATE VIRTUAL TABLE config USING fts3(section, name, value, option, ext, remarks, created)
```

**Rule 评估顺序按 `c6created`(unix 时间戳)DESC,不是 docid**!
证据:docid 660-666 的 bytedance/ixigua DIRECT 规则在 docid=656 FINAL,PROXY 后面,
但 created=1777879447 > FINAL 的 1775477278,实际优先级**高于 FINAL**。

**新加规则的正确做法**:
```sql
INSERT INTO config(section, name, value, option, ext, remarks, created)
VALUES ('rule', 'IP-CIDR', '100.64.0.0/10', 'DIRECT', 'no-resolve', '',
        CAST(strftime('%s','now') AS INTEGER));
```
不指定 docid 会自动 = MAX+1,c6created 给当前时间戳就排到 Rule 段最顶端。
INSERT 必须走 FTS3 虚表 `config`(不是物理表 `config_content`),保证 FTS 索引同步。

完整性校验:
```sql
INSERT INTO config(config) VALUES('integrity-check');  -- FTS3 自检
PRAGMA integrity_check;                                  -- SQLite 自检
```

## tailscale down/up 软修路由(不需要 reboot)

5-06 阿良踩到的另一坑:首次接入后 `route -n get 100.x` 显示 `gateway: 192.168.3.1 / interface: en0`(en0 局域网网关接管),
**TCP 跨机直接 timeout**(虽然 `tailscale ping` 走 UDP P2P 通了,但 SSH/scp 走系统 TCP 路由)。
路由被 utun9(Shadowrocket TUN)抢占。

**[feedback_shadowrocket_skip_proxy.md](feedback_shadowrocket_skip_proxy.md) 4-28 mini 实战记录说必须 reboot 才能让 NetworkExtension reload plist** —
但 air 5-06 实测**不用 reboot**,软修即可:
```bash
/opt/homebrew/bin/tailscale down
sleep 2
/opt/homebrew/bin/tailscale up --hostname=<机器名> --ssh --accept-routes &
sleep 5
# daemon 重新协商,把 100.64.0.0/10 → utun0 注入路由表
netstat -rn -f inet | grep 100.64
# 应显示 100.64/10 utun0 (不是 192.168.3.1 / en0)
```
软修后跨机 SSH 立通(实测 air → mini/neo/neo2 三连 OK)。

差异来源猜测:**首次接入** vs **plist 改完重启** 是两个场景,前者 daemon 重新启动握手就能修,后者 NE 已经吃掉 plist 不更新除非系统重启。

## 4 mac 配置矩阵(2026-05-06 闭环)

| 机器 | docid=2 100.64 | docid=3 100.64 | Rule 段 100.64 | plist HTTPS_PROXY |
|---|---|---|---|---|
| air  | ✅(4-27 阿良) | ✅(4-27 阿良) | ✅(5-06 阿良) | ✅(5-06 阿良) |
| mini | ✅(5-06 阿良补) | ✅ | — | — |
| neo  | ✅ | ✅ | — | — |
| neo2 | ✅ | ✅ | — | — |

5-06 之前 mini 缺 docid=2 ①(只有 ②),理论切 SSID 会复现 air 故障,已 UPDATE FTS3 补齐。

## SSH 互信副效应(注意)

reauth 让 air 拿了新 NodeKey,但**SSH host key 也变了**(macOS 主机名变 air-1 → 改回 air,authorized_keys 不会自动同步)。
表现:air → neo/mini/neo2 SSH `Permission denied (publickey,password)`。
解法:在仍能 SSH 的中转机(台机/其他在线 mac)上把当前 air 的 `~/.ssh/id_ed25519.pub` 灌进目标机的 `~/.ssh/authorized_keys`。
5-06 绣虎从台机一次性把 air 新 pubkey 灌进 mini/neo/neo2,3 机互信复活。

## 不要踩的弯路

- ❌ 改 `/etc/hosts` 写真 IP — 默认路由还是 utun9,TCP 包照样被 Shadowrocket 拦
- ❌ 退出 Shadowrocket — 自己也断网,浏览器无法访问 login.tailscale.com 认证页
- ❌ DNS over HTTPS / `dig @8.8.8.8` — 53 端口被 TUN 劫,直连 DNS 不通
- ❌ `tailscale --reset` / 删 state file — state 干净无济于事,daemon 还是连不上控制面
- ❌ 改 hostname 规避冲突(如 airLE) — admin 后台手改回正确名才能保持 magic DNS 一致
- ❌ 不查就 reauth — air 5-05 出过 3 个影子节点(air / kenchoiair / air-1)admin 后台清理一晚上

## How to apply

- Mac tailscale 首次登录 / reauth / 加新设备失败 + 报 `dial 198.18.x timeout` → 第一反应:plist 注 HTTPS_PROXY
- 跨 SSID 出门回家先做三查 → 详见 [feedback_Mac出门归来三查清单.md](feedback_Mac出门归来三查清单.md)
- 备份原 plist 习惯不能丢:`sudo cp .../tailscaled.plist{,.bak.$(date +%s)}`
- 备份 Shadowrocket db:`cp default.db{,.bak.<标记>_$(date +%Y%m%d_%H%M%S)}`
- 改完用 `tailscale debug prefs | grep Hostname` 确认 prefs 写入,`tailscale status` 看入网状态,
  `tailscale ping <对端 100.x>` 看是 direct 还是 DERP relay

## 实证

2026-05-06 00:30~01:15 air 上从清进程残留 → 删 state file → 改 plist 注 HTTPS_PROXY → daemon bootstrap → 4 秒吐 URL → 缺哥浏览器认证 → admin 端清旧 air/kenchoiair 节点 + 改名 → `tailscale set --ssh --accept-routes` 开 SSH 接路由 → 软修路由 → mini docid=2 补 100.64 → 4 mac SSH 互信验证全通,全流程 ~45 分钟。

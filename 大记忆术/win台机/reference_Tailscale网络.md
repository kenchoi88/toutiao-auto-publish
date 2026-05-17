---
name: Tailscale 网络(kenchoi315@gmail.com tailnet)
description: 6 台机在 Tailscale 上的 hostname / IP 现状,跨机走 100.x.x.x 段(2026-05-18 新台机 kenchoiwinmini 接入)
type: reference
originSessionId: f99b6b5b-4ea0-48d9-baf7-b1b507d56ce3
---
**Tailnet:** `kenchoi315@gmail.com`(同 Google 账号登录)

⚠️ **TS 客户端易失登(2026-05-14 缺哥拍)** — 节点经常需要缺哥手动重新登录(可能 token 过期 / IdP 重新认证 / 客户端 bug)。表现:`tailscale status` 看不全 5 机,或某机 logged out。**跨机前必先 `tailscale status` 实地确认**,看到全员在线了再 ssh,别拿"上次通过"当依据。看到缺哥说"我先登了 TS"= 他刚手动救场,不是 TS 自己稳。

**ACL ssh action = `accept`(2026-05-13 改,5 机互 SSH 免浏览器授权)**
- 默认 `check` 模式每个新 src→dst 12h 内首次都要浏览器开 https://login.tailscale.com/a/... 授权,4 mac 就是 4 次,缺哥要的是「永久免」
- 控制台 ACL `ssh` 段:`{"action": "accept", "src": ["autogroup:member"], "dst": ["autogroup:self"], "users": ["autogroup:nonroot", "root"]}` — 只允许同 tailnet 自己人(就缺哥一人)互通,外人 SSH 不进来
- 以后**新加机/重置 tailnet/重写 ACL** 务必保持 `accept`,改回 `check` 又要点链接;air 那条「首次需浏览器一次性审批」备注已过时

**⚠️ 双门控:控制台绿色 `SSH` 标签 ≠ ACL accept(2026-05-16 neo 实证)**
- ACL `accept` = **tailnet 那道门**:授权某 src→dst 流量进 Tailscale SSH 代理
- 节点 `tailscale set --ssh=true`(或 `up --ssh`) = **节点那道门**:本机起 Tailscale SSH 代理监听,admin 控制台才显示绿色 `SSH` 标签
- 两道门**双重门控**,缺一不可。只有 ACL accept 而节点没 `--ssh`,SSH 仍能走系统 sshd(22 端口)经 Tailscale 网络层通,但走的不是 Tailscale SSH(无审计/无浏览器免授权红利),控制台无标签
- **诊断路径**:看 admin 控制台 https://login.tailscale.com/admin/machines 哪台缺标 → 该机 `tailscale set --ssh=true [--accept-risk=lose-ssh]`(若当前 SSH 会话存在会警告,加 `--accept-risk` 接管)
- **缺哥 5 机 2026-05-16 历史**:台机/air/mini/neo2 都启过 `--ssh`(面板有标),neo 一直只有系统 sshd 走 22(面板无标),今天 `tailscale set --ssh=true` 补齐
- **新加机 / 重装 tailscale** checklist 加这条:`tailscale up --ssh` 而不是 `tailscale up`(避免又漏)


| 机器 / 角色 | Tailscale hostname | Tailscale IP | 备注(2026-04-27) |
|---|---|---|---|
| Win 台机 / 绣虎 | `ken-choi` | 100.86.79.39 | 在线(老台机, SSH 端口 **2222**) |
| 新台机 / 绣虎二代 | `kenchoiwinmini` | **100.95.244.10** | 2026-05-18 阿良立 [[reference_新台机kenchoiwinmini_打通通道]];SSH 用户 **`kench`**(≠ ComputerName `KenChoiWinMini`),**端口 22**(默认),air + 绣虎台机 公钥已灌 administrators_authorized_keys;Win 11 Pro 25H2 全新装;Tailscale SSH server 不支持 Win 端 → 控制台无绿标正常 |
| mini / 东山 | `mini` | 100.70.22.7 | 2026-04-28 force-reauth(阿良瞎搞 Shadowrocket 把 mini 弄掉线 → 重新授权 NodeKey + 新 IP) |
| air / 阿良 | `air` | **100.126.82.58 (2026-05-06 现状,旧 100.67.252.1 已漂)** | 2026-04-27 brew CLI 重装(LaunchDaemon 持久化);旧节点 `kenmacbook-air` 100.102.128.15 = GUI 版僵尸,admin console 删除;**2026-05-01 16:09 实测 idle 在线 + SSH 通**;2026-05-05~06 五小时 Tailscale 故障会话后 IP 漂到 100.126.82.58 |
| neo2 / 左右 | `neo2` | 100.96.153.17 | 2026-04-27 17:50 上线 |
| neo / 小齐+小师弟 | `neo` | 100.68.57.96 | 2026-04-27 18:25 上线;2026-04-28 21:40 admin rename `mac` → `neo`(关 Auto-generate + 手填),根因是该机 macOS HostName=mac,要彻底要 `sudo scutil --set HostName/LocalHostName/ComputerName neo` + 重启 Tailscale daemon |

⚠️ **2026-05-06 抽风教训** — 我 ssh 跨机前没查本表,脑补把 mini=100.86.79.39 / neo=100.70.22.7 / air=100.68.57.96(全错), 实际 100.86=台机自身/100.70=mini/100.68=neo。导致 ssh kenchoios@100.70.22.7 拿 neo 用户名打到 mini → tailscale ssh 拒"failed to look up local user kenchoios"。**真正错的不是 memory(本表全对),是我没用 memory**。

**铁律: 跨机 ssh / scp / tailscale ping 任何带 100.x IP 的命令前,先 `tailscale status` 查一遍真名单或 grep 本表。** 元规则见 `feedback_用上你的记忆.md`。

**Why:** 小旋风段 192.168.50.x 是局域网,跨机访问可走;但腾讯云端(暖树/景清)够不到局域网,长远必须走 Tailscale。Tailscale 100.x.x.x 是统一寻址层,以后 SSH/SMB/任何跨机协议优先用 100.x。

**How to apply:**
- 跨机 SSH **直连 `ssh kenchoiXXX@100.x`**(IP 直连,系统路由把 100.x → utun → Tailscale 隧道),不要用 hostname 也不要用 `tailscale ssh` wrapper(后者反查 hostname 会被 Shadowrocket fake-DNS 拦成 198.18.x)
- 文件传输:`scp kenchoiXXX@100.x:` 走同条隧道
- Win 出去到 4 Mac 全通(Win 端 ProxyOverride 加了 100.64-127.* bypass)
- Mac 主动出去到其它 100.x:**air/neo 已修(改 Shadowrocket [General] tun-excluded-routes 加 100.64.0.0/10)**;mini 待东山修;**neo2 搁置**(没 Claude agent 进驻,不需要)
- 阿良记忆:`feedback_shadowrocket_skip_proxy.md` 说 Mac 版 Shadowrocket TUN 模式必须在 `default.db` 里 UPDATE `general.tun-excluded-routes` 加 100.64.0.0/10 才生效;**部分 mac (mini) sqlite 里没这字段,要走 GUI** 加到「绕过代理」
- Tailscale hostname 已全员统一代号(2026-04-28 admin rename mac → neo);要彻底防被 OS auto 抢回,各机 macOS 系统 HostName 也要 scutil --set 同步成代号
- 看到设备 `offline` → 那台机睡眠 / 关机 / 网断,先确认机器状态再排错
- neo2 已用 LaunchDaemon 持久化(`/Library/LaunchDaemons/com.tailscale.tailscaled.plist`,KeepAlive+RunAtLoad),reboot 自启

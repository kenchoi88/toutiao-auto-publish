---
name: Tailscale 网络(kenchoi315@gmail.com tailnet)
description: 5 台机在 Tailscale 上的 hostname / IP 现状,跨机走 100.x.x.x 段
type: reference
originSessionId: f99b6b5b-4ea0-48d9-baf7-b1b507d56ce3
---
**Tailnet:** `kenchoi315@gmail.com`(同 Google 账号登录)

| 机器 / 角色 | Tailscale hostname | Tailscale IP | 备注(2026-04-27) |
|---|---|---|---|
| Win 台机 / 绣虎 | `ken-choi` | 100.86.79.39 | 在线 |
| mini / 东山 | `mini` | 100.70.22.7 | 2026-04-28 force-reauth(阿良瞎搞 Shadowrocket 把 mini 弄掉线 → 重新授权 NodeKey + 新 IP) |
| air / 阿良 | `air` | 100.67.252.1 | 2026-04-27 brew CLI 重装(LaunchDaemon 持久化);旧节点 `kenmacbook-air` 100.102.128.15 = GUI 版僵尸,admin console 删除 |
| neo2 / 左右 | `neo2` | 100.96.153.17 | 2026-04-27 17:50 上线 |
| neo / 小齐+小师弟 | `neo` | 100.68.57.96 | 2026-04-27 18:25 上线;2026-04-28 21:40 admin rename `mac` → `neo`(关 Auto-generate + 手填),根因是该机 macOS HostName=mac,要彻底要 `sudo scutil --set HostName/LocalHostName/ComputerName neo` + 重启 Tailscale daemon |

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

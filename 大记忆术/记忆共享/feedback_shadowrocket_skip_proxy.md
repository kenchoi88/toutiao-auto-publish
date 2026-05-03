---
name: 跨机 SSH 走 100.x 直连,别用 tailscale ssh wrapper
description: Tailscale 装好后系统路由表本来就把 100.x → utun,直连 ssh kenchoiXXX@100.x 即可;tailscale ssh 命令是 wrapper,会反查 IP→hostname 走系统 ssh,被 Shadowrocket fake-DNS 拦成 198.18.x
type: feedback
originSessionId: f99b6b5b-4ea0-48d9-baf7-b1b507d56ce3
---
**坑:** 用 `tailscale ssh kenair@air` 报 `Connection closed by 198.18.0.x port 22`,以为是 Shadowrocket 拦了 100.64.0.0/10 的 TCP,绕了一大圈改 [General] skip-proxy / tun-excluded-routes 都没用。

**真因(2026-04-28 阿良发现):** Tailscale 装好后系统路由表已经把 `100.x → utun0`(Tailscale 接口)写好了,优先级压过 Shadowrocket TUN。**SSH 隧道一直通**,`nc 100.x 22` 直接拿到 `SSH-2.0-Tailscale` banner。

**真正肇事:** `tailscale ssh` 这个 CLI wrapper 内部把 IP 反查成 hostname 然后调系统 ssh,hostname 解析被 Shadowrocket fake-DNS 拦成 `198.18.x`,所以一直报 `Connection closed by 198.18.x`。**跟 100.x 段被劫持没关系。**

**正解:**
- ✅ **直接 `ssh kenchoiXXX@100.x`**(IP 不走 DNS 解析,系统路由把流量送进 utun)
- ✅ **`scp kenchoiXXX@100.x:`** 文件传输同理
- ❌ **别用 `tailscale ssh` wrapper**(它会反查 hostname → fake DNS 拦)
- ❌ **别用 `tailscale file cp`**(scp 直接走 100.x 即可,不用绕 wrapper)

**Shadowrocket 配置侧:**
- `[General]` 段 `skip-proxy` 加 `100.64.0.0/10` 不需要(路由表压过 Shadowrocket)
- `tun-excluded-routes` 加 `100.64.0.0/10` 也不需要(同上)
- 阿良 air 端加了 `tun-excluded-routes 100.64.0.0/10` 留作"防御性深度",有备份 `default.db.bak.20260427_235332.tun_excl_ts` 可回滚

**How to apply:**
- 跨机 SSH/scp:**永远直连 `kenchoiXXX@100.x`**,不要 hostname,不要 wrapper
- 报 `Connection closed by 198.18.x` 第一反应 = 检查是否在用 `tailscale ssh` wrapper / hostname,而不是改 Shadowrocket 配置
- 4 台 Mac 已实测:kenair@100.67.252.1 / kenchoineo2@100.96.153.17 / kenchoimini@100.70.22.7 / kenchoios@100.68.57.96 全直连 SSH 通(2026-04-28,Shadowrocket 开着不影响)
- Win → mac 都通,反向 mac → Win 也通(Win OpenSSH Server 已 Running)

**Mac 端 plist 改完必须重启 macOS 才生效:**
- Shadowrocket NetworkExtension(MacPacketTunnel)启动时把 plist 里 includedRoutes 写进 utun 路由表,**只 quit Shadowrocket.app 进程不会 reload NE**(NE 由系统 nesessionmanager 管)
- `osascript -e 'quit app "Shadowrocket"'` / `pkill MacPacketTunnel` / `launchctl kickstart tailscaled` 都救不了,**只有 reboot mini macOS 才能让 NE 完整 reload plist**
- 重启后 100.64/10 路由就被 Tailscale utun 拿到(不再被 Shadowrocket utun 抢),100.x SSH 出站立通
- 这条 2026-04-28 在 mini 实战验证(plist 改对但不重启就死循环;reboot 后立刻通)

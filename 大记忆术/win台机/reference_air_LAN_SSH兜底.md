---
name: air Tailscale offline 兜底(LAN IP / mDNS 跳板)
description: air 几乎天天 offline,本机 100.x 不通时三层兜底:① tailscale ping 拿 LAN IP 直连 → ② TSMP 中继不行就走 mini Bonjour mDNS 跳板 → ③ mini 无 air ssh key 走 expect+密码 geng7997
type: reference
originSessionId: 65e7943b-4b50-4d8f-8d15-a85ca3997cff
---
**症状**: `tailscale status` 显示 `air ... idle; offline, last seen Xm ago`,`ssh kenair@100.126.82.58` connect timeout port 22。

**真相**: air Tailscaled 控制平面元数据滞后(没 keepalive 上报)— 但 air 物理上仍在家里 LAN 内,LAN IP 可达。`tailscale ping --c=3 100.126.82.58` 走 LAN 直连 192.168.3.x:41641 ~100ms 通 = 证明 air 实际在线。

**修法**: 直接走家里 LAN IP SSH:

```bash
ssh kenair@192.168.3.7  # air 的 LAN IP (家里 AX3 DHCP)
```

LAN IP 怎么找:
- `tailscale ping --c=3 100.126.82.58` 输出 `pong from air via 192.168.3.7:41641` → LAN IP = 192.168.3.7
- 或 air 桌面 Mac 自查 `ifconfig en0 | grep "inet "`

**Why**: 4 mac 在家里都接 AX3 LAN,即使 Tailscale 控制平面挂了 LAN 段也能直连。Tailscale offline 不等于机器掉线。

**How to apply**: 任何 ssh 100.x mac connect timeout 时,先 `tailscale ping --c=3 <100.x>` 确认 LAN 是否可达,可达就用 LAN IP 走;不可达再考虑切网软修 (tailscale down && up)。

实证 2026-05-11 上午: air SSH 100.126.82.58 timeout,LAN 192.168.3.7 SSH 1 秒通,推 patch_timer_qianN.py 一气呵成。

---

## 二级兜底:LAN IP 也不通 / 本机不在家里 LAN — 走 mini 跳板

**触发**: 台机 `tailscale ping air` 只返回 `via TSMP in Xms` (走 DERP 中继,非 LAN);本机 scp 走 wireguard 走不通;本机不在家里 192.168.3.x 段(出差/咖啡厅)。

**套路** (3 步):

1. **本机 ssh mini** (mini 跟 air 同 LAN,Bonjour 能解析):
   ```bash
   ssh kenchoimini@100.70.22.7 'dns-sd -B _ssh._tcp local. & p=$!; sleep 3; kill $p 2>/dev/null'
   ```
   找到 LAN 上 air 的 mDNS 名 = `KenChoiair.local` (5 机命名规律: `KenChoi<机器>.local`,无连字符无空格)。

2. **mini 走 expect+密码 scp air** (mini 上没配 kenair 的 ssh key,Permission denied + Too many auth failures,所以 OpenSSH 直接登不进,必须强制 password):
   ```bash
   ssh kenchoimini@100.70.22.7 bash <<'OUTER'
   mkdir -p /tmp/air_pull
   expect <<'EOF'
   set timeout 25
   spawn scp -o StrictHostKeyChecking=no -o PreferredAuthentications=password -o NumberOfPasswordPrompts=1 -o PubkeyAuthentication=no kenair@KenChoiair.local:Desktop/<路径>/<文件> /tmp/air_pull/x.txt
   expect { "*assword:*" { send "geng7997\r"; exp_continue } eof }
   EOF
   OUTER
   ```
   密码 = 4 mac 共用 `geng7997` (见 reference_统一密码)。

3. **从 mini /tmp/ scp 回本机** + 用完即清 `rm -rf /tmp/air_pull`(patch完必清.bak规则)。

**Why**: air 控制平面 offline 时,wireguard 直连(LAN/100.x)都可能挂,但 air 物理上还在 LAN 跑 Bonjour 广播 SSH 服务,mini 同段能 mDNS 解析。expect+密码绕过缺 ssh key 的死局。

**How to apply**: air 故障日均一次,先试一级 LAN IP 兜底;TSMP-only / 不在家里 LAN / LAN IP 也 timeout,直接上二级 mini 跳板套路,别再每次重新摸索。

实证 2026-05-11 下午: air offline 13h,TSMP only,通过 mini Bonjour 发现 `KenChoiair.local` + expect+geng7997 scp 走通,系统通知 66KB + 违规提醒 11KB 全拿下。

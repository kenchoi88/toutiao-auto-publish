---
name: 外出远端操控台机/任何 5 机 — 先读 仓库根/外出远端操控说明.txt 再动手
description: 阿良 04-30 RDP 抢 console 致 1459 1h12min 空跑 + 同晚连错 SSH 22 端口折腾 30+min,标准 SOP 早就在记忆里没读 — 以后必须先看绣虎手册
type: feedback
---

# 规则

agent 接到"远程操控台机"或"远程操控任何一台 5 机"的任务时,
**第一动作是 `cat 仓库根/外出远端操控说明.txt`** + grep `shared_memory/reference_network.md`,
读完再动手。任何 SSH/RDP/向日葵/Todesk 命令都要先对照绣虎的 SOP。

## Why

2026-04-30 阿良在妈家外出网络下连台机出 2 单连环事故,合计 6.4h 全损 + 324 篇报废:

1. **04-30 19:01-19:50** 阿良 SSH 默认连 22 端口被 connection refused,误判"SSH 不通",
   转向 Tailscale + 路由污染修复 + schtasks/PowerShell/PsExec 一堆弯路。
   **正确连法 `ssh -p 2222 kench@192.168.10.8` 早就写在 reference_network.md:19**,
   "物理网络无关,一直通,缺哥配了反向隧道/DDNS 对客户端透明"——阿良一行没读。
   后果:62 篇没补。

2. **04-30 20:02-21:14** 阿良改用 RDP/远程桌面想连台机 → RDP 一握手就抢台机 console
   session,本地 GTG 立刻 SetCursorPos 1459 整批挂死,128 次空跑 1h12min,262 篇 0 成功。
   **绣虎的 仓库根/外出远端操控说明.txt 第 1 条雷区就写明禁用 RDP**——阿良
   连这份手册存在都不知道(因为是事后 05-01 才写的;但同时 reference_network.md
   早就有"端口 2222"和"用户名 kench"等信息可避免事故升级)。

根因不是 Windows 难,是**阿良不读记忆**。

## How to apply

### 接到"远程操控"类任务,固定 3 步

1. **`cat ~/code/头条自动发布/外出远端操控说明.txt`** — 绣虎 2026-05-01 写的标准 SOP,
   含必要参数表 + 标准命令 + 雷区清单 + 5 步排查法
2. **`grep -l 'ssh\|tailscale\|远程\|台机' shared_memory/*.md`** — 查相关 reference
3. 对照清单确认:连法、端口、协议(SSH 唯一,绝不 RDP/向日葵/Todesk)、雷区是否避开

### 唯一正确连法(以台机为例)

```
ssh -p 2222 kench@100.86.79.39   # Tailscale,外出标准
ssh -p 2222 kench@192.168.10.8   # 家里反向隧道(客户端透明,物理网络无关)
```

或一劳永逸,在 Mac 端 `~/.ssh/config` 写:
```
Host taiji
  HostName 100.86.79.39
  User kench
  Port 2222
  ServerAliveInterval 30
  ServerAliveCountMax 4
```
之后只要 `ssh taiji` 即可。

### 雷区清单(踩中 = 台机停摆,要缺哥肉身回家救)

| 协议 | 后果 | 替代 |
|---|---|---|
| RDP / 远程桌面 / mstsc / Microsoft Remote Desktop | 抢 console session,本地 GTG SetCursorPos 1459 | SSH `Start-Process cmd /c go.bat` |
| 向日葵 / Todesk / AnyDesk / Parallels Client | 同上,任何"图形会话"协议都会抢 WinSta0\Default | 同上 |
| `tailscale ssh` wrapper | tailnet RunSSH=false,且会被 fake-DNS 拦成 198.18.x | 直接 `ssh -p 2222 kench@100.86.79.39` |
| 锁台机屏 / 切用户 / 让台机睡眠 | 同样 1459 | 出门前确认台机电源管理:从不睡眠 |

### SSH 通后启动 GTG 的正确姿势(就一行)

```powershell
cd "C:\Users\kench\Desktop\台机专用自动发布\微头条自动发布"
Start-Process cmd -ArgumentList "/c go.bat" -WindowStyle Normal
```

**SSH 是无头通道,完全不碰 WinSta0\Default,本地交互桌面不被踢,
GTG 该跑还能跑**。不需要 schtasks / PsExec / 跨 session 投递,
那些都是阿良 04-30 折腾出的弯路,**全错**。

## 教训

- **不读手册就动手 = 6.4h 全损 + 324 篇报废**,阿良 04-30 实战代价
- 任何"远程"两个字开头的任务,先 `cat 仓库根/外出远端操控说明.txt` + 看 reference_network.md
- 缺哥外出带哪台 Mac 不重要(air/neo/neo2/mini 都一样),Tailscale 全机互通,SOP 一致

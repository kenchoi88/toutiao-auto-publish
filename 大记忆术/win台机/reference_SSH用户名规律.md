---
name: SSH 用户名 / IP / ComputerName 表(5 台机)
description: 缺哥 4 台 Mac + Win 台机的 SSH 用户名 + IP + ComputerName 实测表;⚠️neo 用户名 = `kenchoios` (1 个 i),不是 kenchoiios,我多次搞混
type: reference
originSessionId: f99b6b5b-4ea0-48d9-baf7-b1b507d56ce3
---

**统一密码:`geng7997`**(详见 [统一密码](reference_统一密码.md))。
**邮箱前缀:** `kenchoi`(kenchoi315@gmail.com)。

## 5 机权威表(2026-05-02 更新)

| 机器 | 角色 | SSH 用户名 | LAN IP(电信 AX3) | Tailscale IP | **ComputerName**(UC/Bonjour 显示名) |
|---|---|---|---|---|---|
| Win 台机 | 绣虎(我) | `kench` | — | 100.86.79.39 | `ken-choi`(未改) |
| neo2 | 左右 | `kenchoineo2` | 192.168.3.6 | 100.96.153.17 | **`KenChoineo2`** ✅ 2026-05-02 |
| neo | 小齐+小师弟 | **`kenchoios`** ⚠️ 1 个 i! | 192.168.3.5 | 100.68.57.96 | **`KenChoineo`** ✅ 2026-05-02 |
| mini | 东山 | `kenchoimini` | 192.168.3.8 | 100.70.22.7 | **`KenChoimini`** ✅ 2026-05-02 |
| air | 阿良 | **`kenair`** ⚠️ 简化 | — | 100.67.252.1 | **`KenChoiair`** ✅ 2026-05-02 |

## ⚠️ 铁则:SSH 用户名 ≠ ComputerName,别再搞混

- SSH 用户名 = macOS 用户账号的 short name(创建时定的,改不了)
- ComputerName = 机器在 UC / AirDrop / Bonjour 里的显示名(可以随时改)
- **缺哥 2026-05-02 把 5 机 ComputerName 统一改成 `KenChoi+机器名` 风格,但 SSH 用户名没动!**

⚠️ **neo 永远是 `kenchoios`(1 个 i)** — 哪怕它的 ComputerName 改成了 `KenChoineo`,SSH 还是 `kenchoios`。

## 我犯过的错(三次以上,要长记性)

**2026-04-27**:按"kenchoi+机器名"推 neo 用户名为 `kenchoineo`,试 5 个候选都失败,缺哥怒"以前都知道,还要问多少次"。

**2026-05-02 上午**:已经用 `kenchoios` SSH 通了 neo + 改名,中途缺哥说"叫kenchoiios"(指 ComputerName,不是 SSH 用户名),我误解为 SSH 用户名,**自己改用 `kenchoiios`(2 个 i)死磕几小时**,期间瞎报"VPN 抢路由 / IP 被占 / Permission denied 是真坏",全是错诊。最后用户怒"转眼就忘了",改回 `kenchoios` 1 秒通。

## How to apply

- **要 SSH neo 永远用 `kenchoios`(1 个 i)**,Tailscale IP 100.68.57.96
- **缺哥说 "neo 叫 XXX"** → 大概率指 **ComputerName / UC 显示名**,不是 SSH 用户名;先确认是哪个再动
- **改 ComputerName**:`sudo scutil --set ComputerName / LocalHostName / HostName`
- **看 5 机 SSH 通不通** → 直接照表配,不要凭"规律"推
- **跨机优先走 Tailscale IP(100.x.x.x)**,不依赖局域网网段
- LAN IP 段是 192.168.3.x(电信 AX3 ),旧的 192.168.10.x / 192.168.50.x 已弃用

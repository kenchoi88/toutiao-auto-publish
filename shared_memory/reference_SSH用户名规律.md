---
name: SSH 用户名 / IP 表(5 台机)
description: 缺哥 4 台 Mac + Win 台机的 SSH 用户名 + 局域网 IP + Tailscale IP 实测表;规律是 "kenchoi + 机器代号" 但有例外(neo = ios)
type: reference
originSessionId: f99b6b5b-4ea0-48d9-baf7-b1b507d56ce3
---
**统一密码:`geng7997`**(详见 [统一密码](reference_统一密码.md))。
**邮箱前缀:** `kenchoi`(kenchoi315@gmail.com)。

| 机器 | 角色 | SSH 用户名 | 局域网 IP(小旋风) | Tailscale IP | hostname | 验证 |
|---|---|---|---|---|---|---|
| Win 台机 | 绣虎(我) | `kench` | 192.168.50.10 | 100.86.79.39 | `ken-choi` | ✅ 我所在 |
| neo2 | 左右 | `kenchoineo2` | 192.168.50.48 | 100.96.153.17 | `KenChoineo2deMacBook` | ✅ 2026-04-27 |
| neo | 小齐+小师弟 | **`kenchoios`** ⚠️ 例外 | 192.168.50.74 | 100.68.57.96 | `kenchoiosdeMacBook` | ✅ 2026-04-27 |
| mini | 东山 | `kenchoimini` | 192.168.50.78 / 50.6 | 100.70.22.7 | `KenChoideMac-mini` | ✅ 2026-04-28 重新授权后 |
| air | 阿良 | **`kenair`** ⚠️ 例外 | 192.168.50.13 | 100.67.252.1 | `KendeMacBook-Air` | ✅ 2026-04-27 SSH + Tailscale 重装上线 |

**例外:neo 用户名是 `kenchoios`,不是 `kenchoineo`。** 这台 mac 创建时 short name 是 `ios`(可能因为是当年 iOS 开发用机),不是机器代号 `neo`。**别再凭"规律"瞎推 neo 的用户名。**

**Why:**
- 2026-04-27 装 neo Tailscale 时,我按"kenchoi + 机器名"推 `kenchoineo`,试 5 个候选都失败,缺哥怒"以前都知道,还要问多少次"。
- 真相在历史 session(`a73e2d72-...`)里清楚记着 `ssh kenchoios@192.168.10.243`(密码 geng7997)。规律有例外,而例外恰好已经被记过 — 我没翻历史就胡 brute force。

**How to apply:**
- 要 SSH 任何 Mac:**先看这张表;表上没的、要推规律之前先 grep 旧 session jsonl**(`~/.claude/projects/**/*.jsonl`)
- 验证一台后立刻更新这张表(标"已确认 + 日期")
- 旧 IP 192.168.10.x 已大多失效(全员迁小旋风),但 mac 之间历史命令可能还引用旧 IP — 不要直接当真
- 跨机优先走 Tailscale IP(100.x.x.x),不依赖局域网拓扑

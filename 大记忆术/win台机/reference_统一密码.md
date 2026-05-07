---
name: 5 台机登录/sudo 密码 (台机跟 4 mac 不同, 5/7 缺哥纠正)
description: 4 mac 统一密码 geng7997, Win 台机另一个密码 keneunice0816;脚本里 sudo -S 喂密码或 ssh 台机时区分用
type: reference
originSessionId: f99b6b5b-4ea0-48d9-baf7-b1b507d56ce3
---
**4 mac 统一密码: `geng7997`**(2026-04-27 缺哥确认)
**Win 台机密码:    `keneunice0816`**(2026-05-07 缺哥纠正,启动登录用)

⚠ 之前 memory 写"5 机统一 geng7997" 错把台机也归并 — 5/7 缺哥点出台机不同。

适用范围:
- **台机** (kench@Win) → `keneunice0816`
- **air** (kenair@mac) → `geng7997`
- **mini** (kenchoimini@mac) → `geng7997`
- **neo** (kenchoios@mac) → `geng7997`
- **neo2** (kenchoineo2@mac) → `geng7997`

**Why:** 2026-04-27 给 neo2 装 Tailscale 时缺哥发 4 mac 统一密码;5/7 测各机 SSH 时缺哥点出台机本机密码不同(keneunice0816)。

**How to apply:**
- 4 mac 操作:
  ```bash
  echo 'geng7997' | ssh kenchoiXXX@<ip> 'sudo -S <cmd>'
  ```
- 台机本机(Win 启动登录 / SSH 进台机):
  ```bash
  echo 'keneunice0816' | ssh kench@100.86.79.39 '<cmd>'
  ```
- `sudo -S` 走 stdin **绝不**写进 argv(防 `ps` 泄露)
- 不要把密码写进任何会 push 的文件(仓库 / xlsx / 提交信息)
- 这条 memory 是本地 `~/.claude/projects/.../memory/` 下的明文文件 — 跟 ssh 私钥同等级,不要外发
- 如果缺哥说"换密码了",立刻更新这条文件并把新密码替进流程

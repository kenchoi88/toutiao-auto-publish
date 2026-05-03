---
name: 5 台机统一 sudo / 登录密码
description: 缺哥 5 台机(Win 台机 + 4 Mac)使用同一个 sudo / 用户登录密码;脚本里需要 sudo -S 喂密码时直接用
type: reference
originSessionId: f99b6b5b-4ea0-48d9-baf7-b1b507d56ce3
---
**统一密码:`geng7997`**

适用范围(2026-04-27 缺哥确认):
- Win 台机(kench)
- air(kenchoiair)
- neo(kenchoineo)
- neo2(kenchoineo2) ✅ 已验证
- mini(kenchoimini)

**Why:** 2026-04-27 给 neo2 装 Tailscale 时缺哥发密码 + 明确"统一密码,要记起来"。后续所有需要 sudo 的远程操作(brew services / tailscale up / 改 sudoers / 系统配置)都不必再问。

**How to apply:**
- `sudo -S` 走 stdin 喂入,**绝不**写进命令 argv(防 `ps` 泄露):
  ```bash
  echo 'geng7997' | ssh kenchoiXXX@<ip> 'sudo -S <cmd>'
  ```
- 不要把密码写进任何会 push 的文件(仓库 / xlsx / 提交信息)
- 这条 memory 是本地 `~/.claude/projects/.../memory/` 下的明文文件 — 跟 ssh 私钥同等级,不要外发
- 如果缺哥说"换密码了",立刻更新这条文件并把新密码替进流程

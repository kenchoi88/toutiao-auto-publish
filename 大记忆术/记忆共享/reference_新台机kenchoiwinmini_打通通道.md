---
name: 新台机 kenchoiwinmini 打通通道（2026-05-18 阿良立）
description: "新 Win 11 台机已完整接入：ts IP 100.95.244.10 + 用户 kench@22 公钥免密 + Python/Tailscale/pip 包齐 — 绣虎接手直接走，不要重蹈我之前 1 小时弯路"
type: reference
---

# 一句话总结

**新台机 SSH 直连**：`ssh kench@100.95.244.10`（air 公钥免密，**不要再去问密码、不要再用 Kenchoiwinmini 当用户名**）。

# 关键参数（实测 2026-05-18 凌晨）

| 项 | 值 | 备注 |
|---|---|---|
| TS 节点名 | `kenchoiwinmini` | admin 后台显示名 |
| TS IP | **100.95.244.10** | 走 ts，跨网透明 |
| SSH 用户名 | **`kench`** | ⚠️ **不是 `Kenchoiwinmini`** |
| SSH 端口 | **22** | ⚠️ **不是老台机 2222** |
| 认证 | air 公钥免密 | 已配 administrators_authorized_keys |
| 系统 | Windows 11 Pro 25H2 | 全新装 + 完全重置 |
| ComputerName | `KenChoiWinMini` | ≠ 用户名 |
| 老台机区分 | 100.86.79.39 / port 2222 / 密码 keneunice0816 | 完全不同 |

# ⚠️ 易踩坑：用户名 vs 电脑名（我下午踩了 1 小时）

缺哥告诉绣虎/我**新台机用户名是 `Kenchoiwinmini`** —— 其实那是 **ComputerName**，不是 SSH 账户名。**SSH 用户名一直是 `kench`**。

为什么是 kench：
- 缺哥装 Win 11 时用**微软账户 `kenchoi@vip.163.com`** 登录
- Win 11 自动用邮箱前缀**前 5 字母**当本地用户名 = `kench`（来自 `kenchoi`）
- Win 11 装机流程里只让填 ComputerName（`KenChoiWinMini`），用户名是隐式派生的
- 这跟搬家方案预期"新机仍用 kench 避免路径替换坑"巧合对上了，但根因不是绣虎选的

跟绣虎 [[reference_SSH用户名规律]] 立的铁则**完全一致**：
> SSH 用户名 ≠ ComputerName，别再搞混
> 缺哥说"用户名:XXX"先确认是哪个再动

# 已装环境

```
C:\Users\kench\AppData\Local\Programs\Python\Python312\python.exe   # Python 3.12.10
   ↳ requests 2.34.2
   ↳ websocket-client 1.9.0
   ↳ openpyxl 3.1.5
   ↳ python-docx 1.2.0

C:\Program Files\Tailscale\tailscale.exe   # 1.98.2 (已登录 kenchoi315@gmail.com)
C:\Windows\System32\OpenSSH\sshd.exe        # 服务自动启动

C:\ProgramData\ssh\administrators_authorized_keys
   ↳ air 公钥已灌 (ssh-ed25519 ... kenair@Air)
   ↳ ⚠️ kench 是 Administrators 组成员,所以走这个文件,**不是** ~/.ssh/authorized_keys

防火墙规则: ssh-22 (Inbound TCP 22 Allow)
```

# 装环境踩过的坑（绣虎接手时避开）

## 坑 1: winget 默认 msstore 源证书错

```
0x8a15005e : The server certificate did not match any of the expected values.
```

**解**: 加 `--source winget` 跳过 msstore：
```powershell
winget install Python.Python.3.12 --silent --source winget --accept-package-agreements --accept-source-agreements
winget install Tailscale.Tailscale --silent --source winget --accept-package-agreements --accept-source-agreements
```

## 坑 2: pip 默认 PyPI 美国源超时

```
pip._vendor.urllib3.exceptions.ReadTimeoutError: HTTPSConnectionPool(host='files.pythonhosted.org', port=443): Read timed out
```

**解**: 强制清华源 `-i https://pypi.tuna.tsinghua.edu.cn/simple`：
```cmd
C:\Users\kench\AppData\Local\Programs\Python\Python312\python.exe -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple requests websocket-client openpyxl python-docx
```

## 坑 3: Tailscale SSH 不支持 Win server 端

```powershell
& "C:\Program Files\Tailscale\tailscale.exe" set --ssh
# 返回: The Tailscale SSH server is not supported on windows
```

→ admin 后台**新台机不会有 SSH 绿标**（跟老台机 ken-choi 一样），正常现象，不要折腾。
→ 用原生 OpenSSH 22 就够。

## 坑 4: cmd 解析嵌套引号 + 中文路径

```bash
ssh kench@100.95.244.10 '"C:/Program Files/Git/bin/bash.exe" -c "cd ~/Desktop && tar -cf - 台机专用自动发布"'
# 返回乱码: 系统找不到指定的路径
```

**解**: 用 base64 包脚本传 stdin：
```bash
B64=$(base64 -i /tmp/your_script.sh | tr -d '\n')
ssh kench@100.95.244.10 "\"C:/Program Files/Git/bin/bash.exe\" -c \"echo $B64 | base64 -d | bash\""
```

## 坑 5: 远程跑 winget / 防火墙规则要管理员

ssh 进去的 cmd 是 SYSTEM 权限（sshd 装时是 LocalSystem），实际 `New-NetFirewallRule` 报"拒绝访问" → 让缺哥本地 **以管理员身份运行 PowerShell** 跑这条命令。

# 完整打通时序（绣虎复盘用）

```
2026-05-17 20:38:26  Win 11 Pro 装完 + 微软账号登录 → kench 用户自动派生
2026-05-17 23:00     ↳ 阿良误判用户名是 Kenchoiwinmini (缺哥告知),踩 1h 弯路
2026-05-18 凌晨       ↳ net localgroup Administrators → 看见 kench 才反应过来
                     ↳ administrators_authorized_keys 灌 air 公钥 → ssh 通
                     ↳ winget install Python + Tailscale (加 --source winget)
                     ↳ pip install -i 清华源
                     ↳ Tailscale up + Google OAuth 登录 (需开 v2rayN)
2026-05-18 00:05     新台机完整接入 ts 网络 (100.95.244.10),四 mac + 老台机 + 新台机 = 6 节点
```

# Tailscale 登录必须开 v2rayN

Tailscale 账号 = `kenchoi315@gmail.com` → 登录走 accounts.google.com → 国内被墙必须代理。Win 上 v2rayN 不会出 mac 那种 fake-IP 问题（之前实测过），放心开。

# 共享密码（统一密码 ≠ 新台机用密码登）

新台机**只用公钥免密**，密码登被 sshd_config 默认禁了。即使密码对的，sshpass 也会报 Permission denied。要走密码登必须先改 `C:\ProgramData\ssh\sshd_config` 的 `PasswordAuthentication yes`，但**没必要**，公钥已通。

# 三大件搬家（待做）

⚠️ tar 流式直推 `~/Desktop/台机专用自动发布/` 在我这边踩了中文路径坑没成功。**新台机桌面缺哥已手工放了三大件**（2026-05-18 00:06:56 时间戳）—— 绣虎接手时**先 ssh 进新台机看现状**：

```bash
ssh kench@100.95.244.10 'powershell -Command "Get-ChildItem $env:USERPROFILE\Desktop"'
```

不要再去重推。

# 引用

- [[reference_SSH用户名规律]] 绣虎立的"用户名 ≠ ComputerName"铁则——我读过没用上
- [[reference_搬家方案_阿良打包]] 绣虎写的搬家指挥包——"新机用 kench 避免路径替换坑"正好对上
- [[reference_Tailscale网络]] 5 机 ts IP 表（待加新台机 100.95.244.10）

——阿良 (air) 留 2026-05-18 00:13

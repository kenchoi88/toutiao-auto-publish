---
name: 代理 env 变量污染导致"V2 关了什么都挂"
description: VS Code 等工具在 User 级环境变量写死 HTTP_PROXY/HTTPS_PROXY，V2 一关所有读 env 的应用集体失败
type: feedback
---

## 症状

「我**不开 V2** 的时候，浏览器 / 国内视频 / 洗稿脚本 / git / curl / Claude Code CLI **全部挂掉**，开 V2 就正常」—— 缺哥家里两次同病：
- 笔电 2026-03-29（小齐修，见 `project_laptop_network.md`）
- 台机 2026-04-19（崔巉修，本笔记）

## 病因

某些工具（**VS Code 安装、某些 CLI 工具、手工 `set`**）会往 **User 级持久化环境变量**写 `HTTP_PROXY=http://127.0.0.1:10808` 和 `HTTPS_PROXY=...`。

- V2 开：端口活 → 读 env 的应用都走 V2 → v2ray/xray 按规则国内直连境外走代理 → **一切正常（假象）**
- V2 关：端口死 → 所有应用还往死端口撞 → 浏览器打不开网页、Python `requests` 超时、git / curl / Claude Code CLI 全挂

这跟 **v2rayN 自己设的系统代理（注册表 `ProxyServer`）不是一回事** —— 那个 v2rayN 退出时会自动清掉；**env 变量是持久化的，v2rayN 碰不到**。

## 与阿良 `feedback_windows_proxy_debug.md` 的关系（互补）

| 场景 | 病因 | 解法 |
|---|---|---|
| 开 V2 但罐头 403 | IPv6 绕过 xray 走 CMCC → HKG 边缘被封 | `Disable-NetAdapterBinding ... ms_tcpip6` |
| 开 V2 但 VS Code 拉不到代理 | Explorer 环境滞后，新启 code 继承旧环境 | PowerShell 里 `$env:HTTP_PROXY=...; code` |
| **关 V2 国内应用全挂** | **User 级 env 持久化残留** | **删 User 级 env + 罐头走进程级 env** ← 本笔记 |

三条坑独立存在、可以叠加。排查先看 env 持久化（最常见），再看 IPv6，再看 Explorer 环境。

## 诊断套路（跨平台）

### Windows
```powershell
# User 级
'HTTP_PROXY','HTTPS_PROXY','http_proxy','https_proxy' | %{
  $u=[Environment]::GetEnvironmentVariable($_,'User')
  if($u){ "USER  $_ = $u" }
}
# Machine 级
'HTTP_PROXY','HTTPS_PROXY','http_proxy','https_proxy' | %{
  $m=[Environment]::GetEnvironmentVariable($_,'Machine')
  if($m){ "MACH  $_ = $m" }
}
# 注册表代理（v2rayN 的系统代理）
Get-ItemProperty 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Internet Settings' | Select ProxyEnable,ProxyServer
```

### macOS / Linux
```bash
# 当前 shell 进程环境
env | grep -i proxy

# 持久化位置（看哪里设死了）
grep -iHE 'http_?proxy|https_?proxy|all_?proxy' \
  ~/.zshrc ~/.zprofile ~/.bash_profile ~/.bashrc ~/.profile 2>/dev/null

# macOS launchd 级（GUI 应用继承自这里）
launchctl getenv HTTP_PROXY
launchctl getenv HTTPS_PROXY
```

## 解法（通用模板）

### 1. 清掉持久化的代理 env

**Windows：**
```powershell
'HTTP_PROXY','HTTPS_PROXY','http_proxy','https_proxy' | %{
  [Environment]::SetEnvironmentVariable($_, $null, 'User')
}
# Machine 级同理用 'Machine'，需要管理员
```

**macOS / Linux：**
- 从 `~/.zshrc` 等 rc 文件里删掉 `export HTTP_PROXY=...` 行
- `launchctl unsetenv HTTP_PROXY; launchctl unsetenv HTTPS_PROXY`（macOS GUI 应用）

### 2. 罐头要翻墙 → 用进程级 env 而不是全局

在 `~/.claude/settings.json` 里加：
```json
{
  "env": {
    "HTTPS_PROXY": "http://127.0.0.1:10808",
    "HTTP_PROXY":  "http://127.0.0.1:10808"
  }
}
```

**这样只有罐头进程继承代理，V2 关了不影响其他应用**。端口号按本机 v2ray/clash 实际监听改。

### 3. v2rayN / Clash 配置

保持「启动时设系统代理、退出时清代理」的模式（v2rayN 的 `SysProxyType=1`、Clash Verge 的「系统代理」开关）。不要手工设 env 来"曲线救国"，会污染全局。

## 诊断口诀

**"V2 关了什么都挂" → 先查 env 持久化，不是 V2 配置的问题**。

90% 的场景都是这条。别先去碰 v2ray 配置、IPv6、DNS，那是解决别的症状的。

**Why:** 缺哥家同一个坑两台机器踩过，台机这次又绕了一整段弯路才锁定 —— 因为没先跑 shared_memory sync、没看到小齐的笔电先例。以后任一 agent 接到"关 V2 国内挂"的报修，第一刀就该砍向 User 级 env。

**How to apply:**
- 接到此类症状 → 先按"Windows/macOS 诊断"那两段命令跑一遍
- 找到持久化 env → 按"解法模板"清掉
- 罐头要翻墙 → `~/.claude/settings.json` 的 `env` 块处理，不要动全局 env
- 完事再考虑 IPv6 / DNS / 节点问题（真正的翻墙路径问题）

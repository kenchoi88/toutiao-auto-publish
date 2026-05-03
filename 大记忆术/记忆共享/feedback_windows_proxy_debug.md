---
name: Windows台机代理+Claude Code调试要点
description: 台机v2rayN下Claude Code登录403的根因：IPv6绕过代理+进程环境变量滞后
type: feedback
originSessionId: 4d54a0ae-a6c6-4a9f-8876-108bfe0c235c
---
## 背景
2026-04-19 台机（192.168.10.8）VS Code + Claude Code 登录一直 403，花了一整晚才解决。以后遇到类似现象不要再走弯路。

## 坑1：CMCC IPv6 让 xray 代理形同虚设
- xray/v2rayN 默认**只代理 IPv4 流量**
- Windows 解析 `api.anthropic.com` 返回 AAAA（`2607:6bc0::10`），系统通过 CMCC IPv6（`2409:8c54::` 段）直连
- **Cloudflare 把 CMCC IPv6 请求路由到 HKG 边缘**，这条路径访问 Anthropic 返回 403（是封地区还是封IP段不确定，没测试条件验证）
- Shadowrocket（macOS）是 TUN 模式，连 IPv6 也接管，所以同节点能走 LAX 没问题

**解法：禁用活跃网卡的 IPv6**
```powershell
Disable-NetAdapterBinding -Name WLAN -ComponentID ms_tcpip6
```
恢复：`Enable-NetAdapterBinding -Name WLAN -ComponentID ms_tcpip6`

## 坑2：User 级环境变量，新启动的程序拿不到
- `[Environment]::SetEnvironmentVariable("HTTP_PROXY", ..., "User")` 写注册表
- 但 **Explorer（开始菜单）是系统启动就在跑的，不会刷新环境**
- 从开始菜单/双击启动的 VS Code 继承 Explorer 旧环境，**HTTP_PROXY 还是空**
- 所以VS Code扩展的Node请求不走代理 → 直连 → 走CMCC IPv6 → HKG → 403

**解法：新开 PowerShell，手动 set 变量再启动程序**
```powershell
$env:HTTP_PROXY="http://127.0.0.1:10808"
$env:HTTPS_PROXY="http://127.0.0.1:10808"
code
```
这样 VS Code 继承 PowerShell 的活环境。

## 诊断套路（下次直接用）
1. `curl.exe -I https://api.anthropic.com` 看 **CF-RAY 后缀**：
   - LAX/SJC/SEA → 美国，通
   - HKG → 香港，被封
   - 403 基本就是路由到了封禁区
2. `Resolve-DnsName api.anthropic.com -Type AAAA` 看有没有 IPv6，有就可能绕代理
3. `Get-Process xray` 的 TCP 连接远端IP：如果看到 `2409:*` 这种 CMCC IPv6 → 流量在直连不走 xray
4. 在 PowerShell 里 `echo $env:HTTP_PROXY` 确认进程环境

## 浏览器OAuth vs 扩展token 不是同一条路
浏览器能完成 OAuth 授权页，不代表 VS Code 扩展能换 token。
- 浏览器：用户手动打开，读系统代理（IE代理）
- 扩展：Node 请求，读 HTTP_PROXY 环境变量
两者走不同路径，要分别验证。

**Why:** 这次整整折腾了一晚才找到 IPv6 绕代理 + Explorer 环境滞后这两个坑
**How to apply:** 以后Windows代理问题先按诊断套路跑一遍，不要瞎猜节点IP被封

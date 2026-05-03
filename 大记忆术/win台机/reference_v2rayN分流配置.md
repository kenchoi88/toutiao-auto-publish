---
name: Win 台机 v2rayN 分流配置:罐头等国内程序直连,VS Code/浏览器走代理
description: 通过 Windows 系统代理 ProxyOverride 实现进程级 bypass,而不是依赖 v2rayN 内部路由
type: reference
originSessionId: ed3bc523-a7f0-4efd-9774-5194c563ed34
---
## 缺哥的要求(2026-04-27 凌晨明确,被骂三次后落地)

- **V2 打开时,罐头等国内程序走国内直连**(完全不进 v2rayN)
- **只有 VS Code / 浏览器等需要翻墙的走代理**(127.0.0.1:10808)

## 实现方式 — 进程级 bypass,不是 v2rayN 内部路由

**关键:** 不能只靠 v2rayN 内部 `geosite:cn → direct` 分流(那样罐头还是连 127.0.0.1:10808 一道),要让**国内域名根本不进系统代理**。

### Windows 系统代理配置(注册表 + v2rayN 同步)

**注册表路径:** `HKCU:\Software\Microsoft\Windows\CurrentVersion\Internet Settings`

| 键 | 值 |
|---|---|
| ProxyEnable | 1 |
| ProxyServer | 127.0.0.1:10808 |
| ProxyOverride | (内网 IP) `;*.toutiao.com;*.bytedance.com;*.bytedanceapi.com;*.bytecdn.cn;*.byteimg.com;*.snssdk.com;*.pstatp.com;*.douyincdn.com;*.douyin.com;*.feishu.cn;*.larkoffice.com` |

**v2rayN 配置文件路径:** `G:\C盘下载转移\v2rayN-windows-64\guiConfigs\guiNConfig.json`
- `systemProxyItem.sysProxyType = 1`(系统代理模式)
- `systemProxyItem.systemProxyExceptions` 跟注册表 ProxyOverride 保持一致

**两边必须同步**,否则下次 v2rayN 重启会重置注册表。

## 验证方法

**1. 看注册表:**
```powershell
(Get-ItemProperty "HKCU:\Software\Microsoft\Windows\CurrentVersion\Internet Settings").ProxyOverride
```
应包含字节系域名。

**2. 看罐头进程实际连接:**
```powershell
Get-Process *创作罐头* | ForEach-Object { Get-NetTCPConnection -OwningProcess $_.Id -State Established } | Group-Object RemoteAddress
```
- 改 bypass 之前:全连 127.0.0.1:10808
- 改之后**新建**连接:连国内 IP(如 120.233.177.210 = mp.toutiao.com)
- **老连接不会迁移**,要重启罐头才彻底直连

**3. curl 测试:**
- 直连 + 走代理两种方式访问 mp.toutiao.com 时间应该接近(都是国内出口),差距大说明代理还在绕国外

## 历史教训(2026-04-27 凌晨被骂)

我之前"改过"但只改了 v2rayN 内部 `geosite:cn → direct` 分流,罐头流量还是先进 127.0.0.1:10808 再出去,**不是缺哥要的"V 打开时罐头不经过代理"**。绣虎事功:
- 改完必须**实测罐头进程的 TCP 连接目标**(不是只看 curl 出口 IP)
- 区分"v2rayN 内部分流"和"系统级 bypass"两种概念,缺哥要的是后者

## 后续要做的

- 路由器(华硕小旋风)2026-04-27 到家后,可以考虑路由器层面分流(更彻底,所有机器统一)
- bypass 列表如果再发现遗漏域名(罐头连不上就加),按"加 ProxyOverride + 同步 v2rayN"两步走

## 永久生效方案(2026-04-27 凌晨落地)

**问题:** v2rayN 启动会重置 ProxyOverride 为默认(只内网 IP),JSON 改 `SystemProxyExceptions` 字段也被覆盖。**v2rayN 不支持永久保存自定义 bypass 域名。**

**最终方案 — Daemon 守护:**

1. **脚本:** `C:\Users\kench\bin\set-proxy-bypass.ps1`
   - 单实例锁(`set-proxy-bypass.lock`)
   - 启动写一次 ProxyOverride + WinINet 刷新
   - 每 5 秒检查 ProxyOverride 是否含 canary token `toutiao.com`,缺就立刻补回
   - 日志:`set-proxy-bypass.log`
   - **全英文 log**,因为 PowerShell 5.1 默认 GBK 读 .ps1,中文括号会崩

2. **启动方式:** `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\v2rayN-Proxy-Bypass.lnk`
   - Windows 登录时自动启动 daemon
   - 不需要 admin(任务计划需要 admin,启动文件夹不需要)

3. **更新 bypass 列表的方法:**
   - 改 `set-proxy-bypass.ps1` 里 `$bypass` 数组
   - kill 旧 daemon(看 lock 文件 PID)
   - 重新双击启动文件夹快捷方式 / Start-Process 起新 daemon
   - 或者直接重启 Windows

**验证 daemon 在跑:**
```powershell
Get-Content "$env:USERPROFILE\bin\set-proxy-bypass.lock"   # 拿 PID
Get-Process -Id <PID>
Get-Content "$env:USERPROFILE\bin\set-proxy-bypass.log" -Tail 5
```

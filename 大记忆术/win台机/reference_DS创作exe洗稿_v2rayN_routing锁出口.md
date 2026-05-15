---
name: ds-exe-v2rayn-routing
description: "DS创作V1.1.0.exe(Electron)不读 Python env/trust_env,直连行为依赖 Chromium ProxyOverride 缓存,重启即失;真正根治在 v2rayN routing 显式 *.volces.com→direct,锁 xray 出口 IP 为国内(2026-05-16 实证)"
metadata: 
  node_type: memory
  type: reference
  originSessionId: d61da04a-c5e8-43fd-907f-26430855fccc
---

## 核心事实(实证 2026-05-16 00:35)

DS 创作的两套实现走完全不同 net stack:

| 实现 | 文件 | net stack | 受什么控制 |
|---|---|---|---|
| **Python 脚本** | `ds_creator.py` | Python `requests` | env HTTP_PROXY + trust_env(见 [[feedback_程序被代理绑架先查env三件套]] 三件套修法) |
| **Electron exe** | `DS创作V1.1.0.exe` | Chromium net | **完全不读 env**,只读 system proxy + commandLine + userData 缓存 |

**`ds_creator.py` 三层修法(2026-05-12 立的)对 exe 0 作用** — 当时直连成立是因为缺哥跑的是 .py;后来切回 GUI exe 没人意识到行为完全不同。

## 重启后行为不稳

**实证**:DS exe 微头条副本(共用 `%APPDATA%\Roaming\创作罐头\` userData):
- 早启动那次(23:16):TCP 全直连 `192.168.3.9 → 火山 IP` ✓
- 重启之后(00:35):TCP 全走 `127.0.0.1:10808` SOCKS

差异点 = Chromium 首次启动时缓存了 ProxyOverride bypass 决策到 userData,**关进程即失**。同款 exe 同款 userData,**行为偶发性差异**,不能依赖。

## 真正根治 — v2rayN routing 显式规则锁出口

**做法**:在 v2rayN active routing 集(我的是 "V3-绕过大陆(Whitelist)")第一条加:

```json
{
  "OutboundTag": "direct",
  "Domain": [
    "domain:volces.com",
    "domain:volcengine.com",
    "domain:volcengineapi.com",
    "domain:byteintlapi.com",
    "domain:bytedanceapi.com"
  ],
  "Enabled": true,
  "Remarks": "火山/字节 API 强制直连"
}
```

**改 DB 位置**:`G:\C盘下载转移\v2rayN-windows-64\guiConfigs\guiNDB.db`, table `RoutingItem`, **字段 `RuleSet`**(不是 `Url`!), 找 `IsActive=1` 那行 → JSON array → insert at index 0 → 同步更新 `RuleNum` → commit。改完必须**关 v2rayN 重开**(或 GUI "重启服务")让 xray reload。

**效果**(实证):
- DS exe 进程层看依然走 SOCKS `127.0.0.1:10808`(无法改 Electron 顽固行为)
- 但 **xray 出口** `192.168.3.9 → 国内火山 IP`(180.184.47.154 等)
- **风控视角 source IP = 台机出口公网 IP = 国内电信**,跟"真直连"等价

这套**跟 exe net stack 完全解耦** — 无论 Chromium 怎么作,xray routing 配置不动,出口永远国内。

## 多副本 exe single-instance 坑

Electron 默认 single-instance lock 认 `userData 路径`,不认 exe 文件名。**复制 exe 到第 2、3 个目录没用**,启动后会被 IPC 转交给第一个实例然后自己退出,看起来"启动不工作"。

修法:启动加 `--user-data-dir=独立目录路径`,跟现有 userData 隔离。空 userData 首次启动会自动初始化(Network/Cookies/Preferences),登录态会要求重设但 config.ini 里的 API_KEY 直接生效不影响洗稿主链路。

## How to apply

- **看到 DS exe 跑得慢/出口异常** → 第一动作:`Get-NetTCPConnection -OwningProcess <xray-PID>` 看 xray 出口 RemoteAddress 是不是国内 IP,**不要看 DS 自己的 TCP**(它走 SOCKS 是表象)
- **加新 DS 副本**(第 3/4 个目录) → 启动必加 `--user-data-dir=...`,**别只复制 exe** — 锁认 userData
- **永远不要依赖 DS exe 自身直连** — 它的 ProxyOverride bypass 缓存重启就丢
- v2rayN routing DB 字段是 **`RuleSet`** 不是 `Url`(`Url` 是远程规则源 URL,空字符串)

参 [[feedback_程序被代理绑架先查env三件套]] [[reference_v2rayN分流配置]] [[别自己关 V2]]

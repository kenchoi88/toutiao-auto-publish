---
name: q6-pnpcap-ncsi-v2rayn
description: "Win 台机以太网即使 metric 优先且 link Up,仍偶发被 Windows 判 IPv4 无网 fallback 到 WLAN/Q6;三层根因 + 注册表修法(2026-05-16 实证)"
metadata: 
  node_type: memory
  type: reference
  originSessionId: d61da04a-c5e8-43fd-907f-26430855fccc
---

## 现象

Win 台机以太网(Intel I219-V)接 AX3 路由器,**metric 25(WLAN 35)+ link Up 1Gbps + 拿到 192.168.3.x IP**,理论应优先;但**反复出现"被切换到 Q6 WiFi"**,表现为:
- Tailscale 到 air/neo/neo2 走美西 DERP relay(437ms-4724ms),只 mini 偶尔 direct(51ms)
- 推文稿 scp 4 mac 极慢(昨天 2026-05-14 实际痛点)
- 走 ipinfo / curl 看到的出口 IP 跑去 Q6 移动出口

## 三层根因(实证链)

```
Win 节能允许休眠 I219-V (PnPCapabilities=0x10,缺 0x100 bit)
   ↓
网卡反复 link drop & re-identify (NetworkProfile 日志:下午+晚上各一次)
   ↓
NCSI 重新探测 msftconnecttest.com
   ↓
v2rayN routing 没 bypass msftconnecttest → 走 proxy 127.0.0.1:10808
   ↓
proxy 一瞬间不通 → NCSI 标"已连接,IPV4(本地) / IPV6(Internet)"
   ↓
应用判 IPv4 无网 → fallback WLAN/Q6
   ↓
出口跑到 Q6;Tailscale controlplane 也绕代理协商 endpoint
   ↓
4 mac (3 台) P2P 打洞失败 → 美西 DERP
```

## 关键实证

- **PnPCapabilities 位掩码**:
  - `0x10` = PNPCAP_DISABLE_WAKEUP_LINK_CHANGE (link change 唤醒)
  - `0x20` = magic packet 唤醒
  - `0x40` = pattern match 唤醒
  - **`0x100` = PNPCAP_DISABLE_DEVICE_POWER_DOWN ←「允许计算机关闭节电」的反面**
- 注册表路径:`HKLM:\SYSTEM\CurrentControlSet\Control\Class\{4d36e972-e325-11ce-bfc1-08002be10318}\<index>\PnPCapabilities`
  - I219-V 在 index `0010`(机器不同 index 可能不同,按 DriverDesc 匹配)
- `tailscale netcheck` 暴露 `tshttpproxy: using proxy "http://127.0.0.1:10808" for controlplane.tailscale.com`
- v2rayN routing DB:`G:\C盘下载转移\v2rayN-windows-64\guiConfigs\guiNDB.db`,table `RoutingItem`,字段 `IsActive=1` 是激活集
- Win11 PS 5.1 admin shell 里 `Restart-NetAdapter -InterfaceIndex N` 不行,**用 pipe** `Get-NetAdapter -InterfaceIndex 21 | Disable-NetAdapter -Confirm:$false` 然后 enable
- 中文接口名(如"以太网 2")在某些 cmdlet 里编码失败,**优先用 InterfaceIndex 或对象传参**

## 修法(已落 2026-05-16)

**层 1 — 关网卡节电(已做)**: PnPCapabilities `0x10 → 0x110`,然后 disable+enable 网卡触发驱动重读
**层 2 — v2rayN 加 NCSI bypass(待做)**: routing 加 `msftconnecttest.com / msftncsi.com / dns.msftncsi.com` 走 direct
**层 3 — v2rayN 加 Tailscale bypass(待做)**: 加 `*.tailscale.com / *.tailscale.io / login.tailscale.com / controlplane.tailscale.com` 走 direct,根治 Tailscale P2P 走代理协商

## 排查口诀

台机"网线在却被切 Q6"先查 4 件:
1. `Get-NetConnectionProfile` 看以太网 IPv4Connectivity 是否 Internet(若"本地"就是 NCSI 失败)
2. `Get-WinEvent NetworkProfile/Operational` 看以太网最近有没有反复 disconnect/identify
3. 注册表读 PnPCapabilities,缺 0x100 bit 就是节电没禁
4. `tailscale netcheck` 看 `tshttpproxy: using proxy` 行 — 暴露 controlplane 是否被劫持

参 [[reference_Tailscale网络]] [[reference_v2rayN分流配置]]

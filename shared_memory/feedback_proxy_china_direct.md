---
name: 所有 Mac 的 Shadowrocket 必须配置国内直连
description: 缺哥全局硬性要求 — 国内服务全部直连,只有 VSCode 和国外网页走代理
type: feedback
---

# 所有机器的代理配置原则（缺哥 2026-04-06 起的硬性规则,2026-04-30 重申）

**缺哥要求**：所有 Mac（air/mini/neo/neo2/台机）跑的 Shadowrocket / Clash / V2 等代理工具，
**国内服务必须直连(DIRECT)，只有 VSCode 和国外网页才走代理**。

## Why

2026-04-30 阿良在妈家网络下用 air 跑微头条，所有罐头操作卡死(cliclick 点不到/对话框不弹/sheet 不消失)，
折腾 1 小时改 4 版代码都救不了。最终查到根因：
**Shadowrocket 全局代理把 mp.toutiao.com 解析到 198.18.0.24(虚拟 IP)，走 utun9 隧道发国外节点**。
妈家网络上行差，代理路径抖，罐头 webview 长连接超时+丢包 → 一切操作赶在响应回来前发出 → 全卡。

关掉 Shadowrocket 立刻顺畅。**这事缺哥之前已经要求过——所有 Mac 国内服务直连——但 air 的配置漏了**。

## How to apply

### 1. 接手任何机器时,先查代理配置是否合规

```bash
# 看系统代理是不是被全局劫持
scutil --proxy | head -20

# 看代理工具进程
ps aux | grep -iE "shadowrocket|clash|v2ray|surge"

# 看头条/罐头流量是否被劫持
route get mp.toutiao.com    # interface 应是 en0/Wi-Fi,不应是 utun*
ping -c 2 mp.toutiao.com    # 应解析到真实IP(180.x.x.x/110.x.x.x),不应是 198.18.x.x
```

### 2. 发现违规(被代理劫持) → 立即在代理工具里加直连规则

Shadowrocket 配置最顶部(最高优先级)加：

```
# 头条系全部直连
DOMAIN-SUFFIX,toutiao.com,DIRECT
DOMAIN-SUFFIX,bytedance.com,DIRECT
DOMAIN-SUFFIX,czgts.cn,DIRECT
DOMAIN-SUFFIX,snssdk.com,DIRECT
DOMAIN-SUFFIX,toutiaoimg.com,DIRECT
DOMAIN-SUFFIX,toutiaocdn.com,DIRECT
DOMAIN-SUFFIX,pstatp.com,DIRECT
DOMAIN-SUFFIX,bdstatic.com,DIRECT
# 防虚拟 IP 兜底
IP-CIDR,198.18.0.0/16,DIRECT,no-resolve

# 国内常用域名段(GeoIP CN 兜底)
GEOIP,CN,DIRECT
```

### 3. 必须代理的清单(只这些走代理)

- VSCode 扩展(claude code 服务等需要访问 anthropic.com)
- GitHub
- 各种国外开发文档(stackoverflow / mdn / pypi 国外节点等)
- 国外网页浏览

**其他全部走 DIRECT**(头条 / 罐头 / 微信 / 国内 API / 国内 CDN 等)。

### 4. 任何机器看到罐头脚本"响应慢/对话框卡/cliclick 没响应"

**第一反应排查代理**(5 分钟搞定)，不要先去改代码细节。
代理排查清单见上面的 "1. 接手任何机器时" 三步。

## 教训

阿良 04-30 浪费 1 小时改了 4 版代码(循环 keystroke / click button / debug 按钮列表),
全是网络锅，跟代码无关。**后续 agent 别再走这弯路**。

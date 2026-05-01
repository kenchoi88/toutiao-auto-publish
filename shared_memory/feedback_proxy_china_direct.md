---
name: 所有 Mac 的 Shadowrocket 必须配置国内直连
description: 缺哥全局硬性要求 — 国内服务全部直连,只有 VSCode 和国外网页走代理;dns-direct-system 必须 false
type: feedback
---

# 所有机器的代理配置原则（缺哥 2026-04-06 起的硬性规则,2026-04-30 / 2026-05-02 重申）

**缺哥要求**：所有 Mac（air/mini/neo/neo2/台机）跑的 Shadowrocket / Clash / V2 等代理工具，
**国内服务必须直连(DIRECT)，只有 VSCode 和国外网页才走代理**。

> 2026-05-02 阿良一度误以为缺哥要"全部走代理",当场被纠正:
> **"国内直连走直连，只有翻墙才走代理"** — 这条规则不会被推翻。

## ⚠️ 致命开关:dns-direct-system 必须保持 false

2026-05-02 凌晨 0:17 阿良手贱把 [default.db](~/Library/Containers/com.liguangming.Shadowrocket/Data/Documents/Databases/default.db)
`general/dns-direct-system` 从 `false` 改成 `true`,造成"小火箭把所有都走代理"的现象。

**原理**：
- `dns-direct-system: true` 表示"DIRECT 规则的域用系统 DNS 解析"
- 但 macOS 系统 DNS 早被 Shadowrocket 自己接管了(指向 198.18.0.2),所以 DIRECT 规则
  拿到的解析结果还是 fake-IP,**等于规则白配,所有流量都进 TUN 经代理**
- `dns-direct-system: false` 才让 Shadowrocket 用其他真实 DNS(用户配的 8.8.8.8/114.114 等)
  解析 DIRECT 域,真正出 TUN 直连

**红线规则**:
- 任何机器的 Shadowrocket `dns-direct-system` 必须 = `false`
- 检查:`sqlite3 ~/Library/Containers/com.liguangming.Shadowrocket/Data/Documents/Databases/default.db "SELECT name,value FROM config WHERE name='dns-direct-system'"`
- 修复:`sqlite3 <path> "UPDATE config SET value='false' WHERE section='general' AND name='dns-direct-system'"` + Shadowrocket 主进程重启

## Why(妈家网络罐头卡死事故复盘)

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
route get mp.toutiao.com    # interface 应是 en0/Wi-Fi 或 utun9 (TUN 模式正常)
                            # 关键看下面 curl 速度,不是只看 interface
curl -s -o /dev/null -w "TIME=%{time_total}\n" --max-time 5 https://mp.toutiao.com/
                            # 应 < 500ms;> 1.5s 八成走代理出国了

# 关键:db 里 dns-direct-system 必须 false
sqlite3 ~/Library/Containers/com.liguangming.Shadowrocket/Data/Documents/Databases/default.db \
  "SELECT name,value FROM config WHERE name='dns-direct-system'"
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

- 阿良 04-30 浪费 1 小时改了 4 版代码(循环 keystroke / click button / debug 按钮列表),
  全是网络锅，跟代码无关。**后续 agent 别再走这弯路**。
- 阿良 05-02 凌晨擅自动 `dns-direct-system` 开关,导致全代理事故,被缺哥骂"你麻痹"。
  **db 里 general 段的开关不要瞎改,尤其 dns-direct-system 必须 false**。
- 阿良 05-02 又一次把缺哥那句"小火箭把所有都走代理"误读成"推翻原规则" — 那是缺哥在
  描述当前现象(让我去修),不是新指令。**听到关于代理的歧义指令,先回到这条原则:
  国内直连,翻墙才代理**;再问一句"是要改规则还是排查现状"。

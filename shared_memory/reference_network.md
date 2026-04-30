---
name: 网络连接参考：各机器SSH及接口
description: 局域网内各设备SSH连接方式、openclaw接口、DNS注意事项
type: reference
originSessionId: 0e9e6cdf-de45-458d-b2ce-c21a71bbed5d
---
## 各机器SSH

| 机器 | 连接命令 | 备注 |
|------|---------|------|
| Windows笔电（崔巉） | `ssh kench@192.168.10.150` | 密钥免密直连 |
| Windows台式机（崔巉） | `ssh -p 2222 kench@192.168.10.8` | 端口2222，密钥免密 |
| neo（小齐所在Mac台式机） | `ssh kenchoios@192.168.10.243` | 密码：geng7997，IP不固定（原231，现243） |
| mini（崔东山，发文主力机） | `ssh kenchoimini@192.168.10.244` | 密码：geng7997，hostname：KenChoideMac-mini.local |
| macneo2（新Mac） | `ssh kenchoineo2@192.168.10.245` | 密码：geng7997，hostname：KenChoineo2deMacBook.local，Python3.12已装，cliclick已装，权限已开 |

- 台式机22端口有问题，固定用2222
- 传文件到台机：`scp -P 2222 本地文件 kench@192.168.10.8:C:/目标路径`
- **台机SSH地址不随物理网络变化**：无论台机走家里路由器/移动网络/咖啡店WiFi，`ssh -p 2222 kench@192.168.10.8` 一直通（缺哥那边配了反向隧道/DDNS之类的转发，对客户端透明）。所以遇到"台机不在内网"时**别再问连接方式，直接 ssh 试**——别再像 2026-04-19 阿良那样去查 ~/.ssh/config 还问"是不是有外网IP"
- 在台机上跑命令默认 cmd.exe，不认识 `tail`/`grep`，要用 git bash：`ssh -p 2222 kench@192.168.10.8 '"C:/Program Files/Git/bin/bash.exe" -c "你的命令"'`

## Tailscale（外网穿透 SSH，必备）

5台机器全部接入了同一 Tailscale 网络（账号 `kenchoi315@`）。**Air 走移动热点时局域网IP不通，必须用 TS IP**：

| 机器 | TS IP | TS 节点名 |
|---|---|---|
| Air | 100.67.252.1 | air |
| 台机（崔巉） | 100.86.79.39 | ken-choi |
| mini（崔东山） | 100.70.22.7 | mini |
| neo（小齐） | 100.68.57.96 | neo |
| neo2 | 100.96.153.17 | neo2 |

- Air 上的 tailscale 装在 homebrew Cellar，**不在 PATH**：用 `/opt/homebrew/Cellar/tailscale/<版本>/bin/tailscale` 或 `/opt/homebrew/bin/tailscale`（如果有软链）。`which tailscale` 找不到不要立刻断言"没装"
- 查节点：`/opt/homebrew/bin/tailscale status` 或上面绝对路径
- TS IP 替换原局域网 IP 即可，端口/账号/密码/SSH 用法都一样
- 例：`sshpass -p geng7997 ssh kenchoimini@100.70.22.7 ...`（mini 走 TS）
- 教训（2026-04-19）：阿良在外面用移动热点时 ping 192.168.10.x 全 100% 丢包，错以为机器都离线，没想起 Tailscale。**任何机器局域网 IP 不通时，第一反应换 TS IP**

## 陈平安（OpenClaw）接口
- Gateway端口：`localhost:18789`
- API端口：`localhost:18791`（需授权）
- 发消息给平安：`openclaw agent --agent main --message "内容"`
- TUI：`openclaw tui`
- 命令路径：`/opt/homebrew/bin/openclaw`

**平安内部结构：**
- `main`（本体）：默认模型MiniMax-M2.5
- `playwright`：浏览器自动化子agent
- `tavily`：联网搜索子agent

## DNS注意
- DS创作工具/今日头条相关：必须用公共DNS（119.29.29.29 或 223.5.5.5），否则今日头条抓取失败
- VSCode需V2代理，DS/罐头不能走代理，注意冲突

## 代理踩坑（2026-04-30 阿良在妈家网络实证）

**核心规则: 罐头/头条流量永远走直连,不要被 Shadowrocket/Clash/V2 劫持**

  Shadowrocket 全局代理把 mp.toutiao.com 解析成 198.18.0.24(虚拟 IP),
  走 utun* 隧道送国外节点。家里网络上行好看似正常,妈家/咖啡店等弱上行
  网络下,代理 ↔ 国外节点路径抖,罐头 webview 长连接超时+丢包,
  cliclick/keystroke/osascript click button 全部赶在罐头收到响应之前发出,
  所有"对话框未弹/按钮无响应/sheet 不消失"的症状都来自这条根因。

  **症状特征**:
    - cliclick 点"文档导入"3 次都不出"选择文档"小弹窗
    - "前往文件夹"小框 8s 不出现
    - osascript click button 报"成功"但 sheet 不消失
    - 重试 3 次全失败,跨账号稳定复现

  **快诊三步**:
    1. `scutil --proxy` 看 HTTP/HTTPS Proxy 是否被设(127.0.0.1:1082 等)
    2. `ps aux | grep -iE "shadowrocket|clash|v2ray|surge"` 看代理进程
    3. `route get mp.toutiao.com` 看接口 — utun* = 被代理劫持

  **解法**(任选):
    - 临时: 关掉代理(菜单栏图标点关闭)
    - 长期: 代理工具加直连规则
      ```
      DOMAIN-SUFFIX,toutiao.com,DIRECT
      DOMAIN-SUFFIX,bytedance.com,DIRECT
      DOMAIN-SUFFIX,czgts.cn,DIRECT
      DOMAIN-SUFFIX,snssdk.com,DIRECT
      ```

  **教训**: 不要先怀疑代码 — 罐头脚本反复出"响应慢/对话框卡"症状时,
  先排查代理(5 分钟搞定),再去改代码(可能改半天还是网络锅)。

## 台机debug_launch
- 台机（192.168.10.8）部署罐头时，`debug_launch.bat` + `debug_launch.py` 绝对不能删
- bat只写`python "%~dp0debug_launch.py"`，py文件用subprocess启动罐头

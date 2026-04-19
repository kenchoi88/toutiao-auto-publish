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

## 台机debug_launch
- 台机（192.168.10.8）部署罐头时，`debug_launch.bat` + `debug_launch.py` 绝对不能删
- bat只写`python "%~dp0debug_launch.py"`，py文件用subprocess启动罐头

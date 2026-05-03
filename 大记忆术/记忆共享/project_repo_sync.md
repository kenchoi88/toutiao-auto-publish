---
name: 单仓库跨机同步格局
description: 5台机器共用 toutiao-auto-publish 仓库作为跨机同步通道
type: project
originSessionId: 4d54a0ae-a6c6-4a9f-8876-108bfe0c235c
---
## 仓库
`kenchoi88/toutiao-auto-publish`（GitHub 公共），克隆到各机 `~/code/头条自动发布/`

## 5台机器
| 机器 | 状态 |
|------|------|
| Air（阿良） | 已clone，主力开发机 |
| neo（小齐所在Mac台式机） | 已clone（2026-04-19） |
| mini（崔东山） | 已clone（2026-04-19） |
| 台机（Windows台式机，崔巉） | 待clone |
| neo2（新Mac） | 待装 VS Code 后再clone |

## 用途
不只是"头条自动发布"这一个项目——这是所有机器的**统一同步通道**。即使某台机不跑 MCN 脚本，也会用这个仓库做别的事同步代码。

## Air 特殊设置
`~/Desktop/MCN数据` → `~/code/头条自动发布/MCN数据` 软链接。桌面访问不变，文件实体在仓库里。
xlsx数据文件靠 `.gitignore` 的 `*.xlsx` 不入仓库，只在 Air 上保存。

**Why:** 缺哥原本桌面放脚本、仓库空着；现在统一。2026-04-19 定型
**How to apply:** 任何机器改代码都 `git push`，其他机器 `git pull` 同步；仓库可加新子目录承载别的工具

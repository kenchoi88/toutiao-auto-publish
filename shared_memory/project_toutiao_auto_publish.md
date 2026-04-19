---
name: 头条自动发布项目
description: 用户的"头条自动发布"项目基本信息——本地路径、GitHub 仓库、账号
type: project
originSessionId: 4d54a0ae-a6c6-4a9f-8876-108bfe0c235c
---
用户正在 `/Users/kenair/code/头条自动发布` 目录开发"头条自动发布"工具，所有工作都在这个目录进行。

## 基础设施
- 本地路径：`/Users/kenair/code/头条自动发布`
- GitHub 仓库（公共）：https://github.com/kenchoi88/toutiao-auto-publish
- GitHub 账号：kenchoi88
- 主分支：main
- 2026-04-18 完成项目脚手架（git init + 首次推送），仅有 README.md 和 .gitignore，尚未开始功能开发

## 项目立项（2026-04-18，未开工）
**核心思路**：把头条爆款作者"蒸馏"成独立的 Claude Skill，作为自动发布的内容引擎。

**参考项目**：[titanwings/colleague-skill](https://github.com/titanwings/colleague-skill)（即用户口中的"蒸馏"项目）——把人的沟通材料+主观描述蒸馏成 Claude Code Skill，遵循 AgentSkills 标准，有 Work+Persona 双层结构、支持增量追加材料和对话修正。

**已定决策**：
- 一个头条作者 = 一个独立 Skill（不合并、不互相污染）
- 输入：用户会提供每个作者的若干篇（"几百篇"量级）文章作为素材

**待定**（下次接着问用户）：
1. 素材投喂形式：(a) 用户自己复制成文件 (b) 给头条号主页让我爬 (c) 其他
2. 最终用法：(a) 给主题→生成全文 (b) 给热点→生成选题+标题+全文 (c) 都要
3. 蒸馏维度建议默认全要且分层存储：标题套路 / 选题偏好 / 写作风格 / 爆款公式

**Why:** 用户明确"现在不用做，先立项"——下次对话要先收齐这两个答案再动手，不要擅自实现。

**How to apply:** 下次用户回到这个项目时，先复述立项状态确认没偏，再追问待定项 1 和 2。不要在未对齐前搭代码结构。

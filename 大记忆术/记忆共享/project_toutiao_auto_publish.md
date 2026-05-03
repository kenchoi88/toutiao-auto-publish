---
name: 头条自动发布项目
description: 用户的"头条自动发布"项目——本地路径、GitHub 仓库、蒸馏子项目的落地状态
type: project
originSessionId: 4d54a0ae-a6c6-4a9f-8876-108bfe0c235c
---
用户在 `~/code/头条自动发布` 开发"头条自动发布"工具链。

## 基础设施
- 本地路径（台机）：`C:\Users\kench\code\头条自动发布`
- GitHub 仓库（公共）：https://github.com/kenchoi88/toutiao-auto-publish
- GitHub 账号：kenchoi88
- 主分支：main

## 蒸馏子项目（2026-04-20 首轮 AB 测试落地）

**思路**：把头条爆款作者蒸馏成独立 Claude Skill，作为内容引擎。

**框架**：`titanwings/colleague-skill`（即 dot-skill）。本机装在 `~/.claude/skills/dot-skill/`，触发命令 `/dot-skill`。

**已完成**：
- 抓取脚本：`蒸馏/抓取素材.py` —— 读头条号后台导出的 xls，逐篇抓 `m.toutiao.com/a{gid}/` 的 SSR 页拿标题+description，输出 JSON+MD
- 首个 skill：唐驳虎主笔（`dot-skill/skills/celebrity/tang-bo-hu-zhu-bi/`），基于 79 篇样本（4/1-4/18）蒸馏，含 meta.json / persona.md / work.md
- 稿件生成：`蒸馏/生成稿件.py` —— 按 skill 风格写稿，可从火山洗稿 docx 提图组装到新 docx（`extract_images` + `build_docx`）

**2026-04-20 首轮 AB 测试方案**：
- 选题源：武事汇 4/14-4/17 的 3 条真事件（伊朗海峡/美军开火令/欧尔班败选）
- A 号发火山洗稿版（生活化口语体 ~600 字，由 DS创作 exe 跑出）
- B 号发唐驳虎风格版（评论员体 ~1400 字，由 `生成稿件.py` 跑出，复用火山下好的图）
- 错时发避免头条跨账号判雷同
- 评估三维：原创分、阅读量、违规率

**Why:** 火山洗稿是"换叙述主体"的反向洗稿路线（标题不改+正文彻底口语化），我走的是"换选题角度+换结构"的风格蒸馏路线。两条路过原创的机制不同，明天数据决定后续主推哪条。

**How to apply:** 下次接手此项目的 agent 要先看 `蒸馏/生成稿件.py` 的 PIECES 结构——稿件数据与逻辑混在一起，真正规模化时要拆成"skill 产文 → 独立数据文件 → 组装器"三层。暂时先用当前单文件模式跑通闭环。

## 反面清单（别再踩）
- xls 用 xlrd 不是 openpyxl（openpyxl 只支持 xlsx）
- PC 端 toutiao.com/item/ 返回 JS 骨架没内容，必须走 `m.toutiao.com/a{gid}/` 移动 SSR
- 头条摘要接口对连续请求有限流，抓 70+ 篇后会 size=0，需加 sleep 或接受部分失败

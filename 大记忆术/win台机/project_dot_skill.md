---
name: 蒸馏项目 = dot-skill
description: 缺哥跟阿良立的"蒸馏"项目 = github.com/titanwings/colleague-skill,装在 ~/.claude/skills/dot-skill,触发 /dot-skill
type: project
originSessionId: 8b4b8348-f64c-4f9b-bf56-8c6844ea83ba
---
# 蒸馏 = dot-skill

缺哥说"蒸馏 / 蒸馏一个 XX / 立 skill" → 对应 dot-skill 工作流,不再追问。

## 作用
把"人"(同事 / 关系 / 名人)**蒸馏**成一个像 TA 一样说话、思考的 Claude Skill,用聊天记录、文档、访谈等素材喂养。

## 本机安装(2026-04-19,2026-05-01 实证仍在)
- 路径:`C:\Users\kench\.claude\skills\dot-skill\`
- 上游:`github.com/titanwings/colleague-skill`(项目内部名 dot-skill)
- 必需依赖:`requests>=2.28.0` ✅
- 可选依赖:pypinyin / playwright / slack-sdk / python-docx / openpyxl — 用时再装
- 触发:`/dot-skill`

**Why:** 2026-04-19 缺哥跟阿良(air)立项,air 装了台机也同步装,保持团队一致。

**How to apply:**
- 跑 `tools/` 或 `prompts/` 里的脚本不要自己 `cd` 到别的路径,SKILL.md 工作目录就是 skill 根
- 更新上游:`cd ~/.claude/skills/dot-skill && git pull`(GitHub 现已直连可达,不必走 V2 SOCKS)
- 扩展采集源(飞书/钉钉/Slack/Word/Excel)时回头装对应可选依赖

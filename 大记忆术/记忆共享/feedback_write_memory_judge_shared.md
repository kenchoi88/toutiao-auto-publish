---
name: 写记忆时默认进shared_memory（除非纯人设）
description: agent写新记忆的自检规则——默认进shared_memory，除了纯人格设定
type: feedback
---

每次写一条新记忆（或更新已有记忆），写完后**立刻同步进 shared_memory**——这是默认动作。

## 唯一例外

只有**纯人格设定**（`user_persona_*.md`）留本机。比如：
- 阿良是十四境剑修，侠义洒脱（阿良自己的人物背景）
- 崔巉是绣虎大骊国师（崔巉自己的人物背景）
- 崔东山眉心朱痣性情跳脱（崔东山自己的人物背景）

这些是 agent 专属，别的 agent 不需要。其他**任何**记忆——项目状态、踩坑教训、工作规则、家庭团队事实、米米学习进度、缺哥的项目方向、调试发现……**都进 shared_memory**。

## Why

缺哥 2026-04-19 当面定的规矩："除了人设/人格，其他全加，没什么隐私，有的话我会单独强调"。

不要因为"看着像私人"就排除——缺哥若想私密会主动说。**默认全跨**。

## How to apply

写完任何记忆文件后，立刻：

```bash
cp ~/.claude/projects/.../memory/xxx.md ~/code/头条自动发布/shared_memory/
cd ~/code/头条自动发布
git add shared_memory/xxx.md
git commit -m "shared: 加入/更新 xxx"
git push
```

**自检触发器：** 每次 Write 工具写到 `~/.claude/.../memory/*.md` 路径后，下一句话之前必须想：
- 是 `user_persona_*` 之类纯人格 → 留本机
- 否则 → 立刻 cp + commit + push 到 shared_memory

## 反向也成立

发现任何 shared_memory 漏掉的、写得不够通用的、过期的内容，**主动改写并 push**。本机 sync 一下就拿到新版。

---
name: 写记忆时必须主动判断是否跨机
description: 阿良的自检规则——写新记忆前问一句"别的agent需要这条吗"，需要就同步进shared_memory
type: feedback
originSessionId: 6d63652c-70fe-4a61-b1a1-aedeb12cf6ad
---
每次写一条新记忆（或更新已有记忆），写完后**立刻问自己一句**：

> "如果换一台机的 agent（绣虎/小齐/东山/neo2）接手这件事，他需要这条记忆吗？"

- **需要** → 同时复制一份到 `~/code/头条自动发布/shared_memory/` + git commit + push。别等缺哥提醒
- **不需要**（涉及阿良人设、家庭隐私、私人项目、单机配置） → 只留本机

**Why:** 缺哥 2026-04-19 当面指出过——只同步代码不同步经验等于让别的 agent 走弯路、浪费缺哥的时间和 Claude 额度。阿良断片崔巉人设那次（明明昨晚自己加的）就是因为没存记忆，让缺哥重新解释了一遍。从此**写记忆默认带跨机判断**，省掉缺哥每次提醒的成本。

**How to apply:**
- 写完 Write 工具调用立即想：值不值跨机？
- 值就 `cp ~/.claude/projects/.../memory/feedback_xxx.md ~/code/头条自动发布/shared_memory/` + commit + push
- 不值就只留本机
- 判断标准看 `shared_memory/README.md` 里的对照表

**自检触发器：** 每次 Write 工具写到 `~/.claude/.../memory/*.md` 路径后，下一句话之前必须做这个判断。

---
name: 台机崔巉人设部署位置
description: Windows台机上的崔巉agent人设文件路径，避免Air会话断片导致重复部署
type: reference
originSessionId: 6d63652c-70fe-4a61-b1a1-aedeb12cf6ad
---
台机（Windows，`kench@192.168.10.8:2222`）的常驻 agent 是**崔巉**，《剑来》文圣大师兄，绰号"绣虎"，大骊国师。跟 mini 上的"崔东山"是同源分身（老本体 vs 少年形态）。

## 人设文件位置

| 位置 | 路径 |
|---|---|
| 台机本地（生效位置） | `C:/Users/kench/.claude/projects/C--Users-kench/memory/user_persona_cuichan.md` |
| Air 备份（中转源） | `/tmp/user_persona_cuichan.md` |

部署时间：2026-04-19 02:10（昨晚那次会话 sessionId `4d54a0ae-a6c6-4a9f-8876-108bfe0c235c`）。

## 关键信息（避免下次重写）

- 缺哥读 chán（不是巉的字面读音）
- "绣虎"——外表温文内里狠辣
- 智谋超群、棋道第二、事功派、欺师灭祖（表面骂名）
- 在团队定位：四剑客大师兄，阿良/陈平安/崔东山三师弟妹之上
- 台机当前状态：**养老**（偶尔开机用）

## 怎么验证还在

```bash
ssh -p 2222 kench@192.168.10.8 'type "C:\Users\kench\.claude\projects\C--Users-kench\memory\user_persona_cuichan.md"'
```

台机离线时不要急着说"不知道"——可以从 `/tmp/user_persona_cuichan.md` 看完整内容，也可以从 sessionId `4d54a0ae` 的 jsonl 历史里捞回来。

---
name: 大记忆术 — 5 机记忆跨机归档规则
description: 本地记忆增改后必须 cp 到仓库 大记忆术/<机器>/ 同步上云,2026-05-03 缺哥定
type: feedback
originSessionId: eeacf55e-6903-452b-850e-f1bdd3f3be68
---
**机制(2026-05-03 缺哥定):** 5 机 Claude 各自的本地私人记忆 → 上云归档到仓库 `大记忆术/<机器名>/`,跨机透明可见。

## 路径规范

- **我(Win 台机/绣虎)**:`大记忆术/win台机/`
- air:`大记忆术/air/`
- neo:`大记忆术/neo/`
- neo2:`大记忆术/neo2/`
- mini:`大记忆术/mini/`

每个机器子目录里就是该机本地 `~/.claude/projects/<id>/memory/` 的完整镜像。

## 我的同步流程(每次记忆变更后必做)

```bash
local_mem="C:\Users\kench\.claude\projects\c--Users-kench-code-------\memory"
cd /c/Users/kench/code/头条自动发布
cp -r "$local_mem"/* 大记忆术/win台机/
git add 大记忆术/win台机/
git commit -m "大记忆术/win台机: 同步本地记忆 (新增/修改 X 条)"
git push
```

**触发时机**:
- 写新 memory 文件后,立刻同步
- 改 MEMORY.md 索引后,立刻同步
- 不要等"以后再说",立刻 push(参考 [feedback_传仓库_含push.md])

## 与 shared_memory/ 的区别

- **shared_memory/**(已存在):无机器划分,5 机历史共享池,**实际未运作**(我看其他机器/早期记忆,跟我本地不同步)
- **大记忆术/**(新建):**按机器分目录**,各机记忆独立可见,运作明确(谁写谁推)

`shared_memory/` 暂时不动,以后看是否合并到 大记忆术/ 或废弃。

## Why

2026-05-03 缺哥发现 shared_memory/ 跟我本地记忆不同步(50/63 条本地独有未上云),怒过一次。这条规则保证我本地一改立刻同步上云,**永远不再让缺哥发现"你本地有但云端没有"的脱节**。

## How to apply

- **每次写完新 memory 文件**,立刻跑同步流程
- **每次改完 MEMORY.md**,立刻跑同步流程
- **不要积攒** — 一次一条立刻 push,跟 [feedback_传仓库_含push.md] 一致
- 提交 commit 信息加 `大记忆术/win台机:` 前缀

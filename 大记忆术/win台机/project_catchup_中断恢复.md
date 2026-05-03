---
name: catchup.py 中断恢复(本地副本,真版在 shared_memory)
description: 三大件中断后启动 catchup.py 自动算漏数 + 环形排序写白名单,缺 N 补 N
type: project
originSessionId: 6198d8da-e501-4a0b-b8de-45446700703e
---
真版在 `c:\Users\kench\code\头条自动发布\shared_memory\project_catchup_中断恢复.md`。

**核心 4 步**:
1. 读最新 log → 找断点账号 + 当前大循环/小轮
2. 算漏数:优先「待补漏」sheet,fallback 看 log 算 quota - 已成功
3. 环形重排:`items[idx:] + items[:idx]`
4. 写白名单 + 备份

**适配**:
- 微头条 5 小轮 / 文章 3 小轮 / 文章定时通过 文章自动发布 catchup.py 补
- gtg_batch.py 必须 v1101.5+(按 xlsx 顺序跑)

**用户 3 步**:cd 件目录 → python3 catchup.py → 双击 go.command

诞生于 2026-05-02 04:09 电信断网事件(全队 394 个账号误判硬终止),沉淀成一键工具。

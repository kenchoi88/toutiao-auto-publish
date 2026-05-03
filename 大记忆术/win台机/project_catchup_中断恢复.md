---
name: catchup.py 中断恢复(本地副本,真版在 shared_memory)
description: 三大件中断后启动 catchup.py 自动算漏数 + 环形排序写白名单,缺 N 补 N
type: project
originSessionId: 6198d8da-e501-4a0b-b8de-45446700703e
---
真版在 `c:\Users\kench\code\头条自动发布\shared_memory\project_catchup_中断恢复.md`。

## v1101.5(2026-05-02)路线 — catchup.py 独立脚本(已被 v1102 取代,留作 backup)

**核心 4 步**:
1. 读最新 log → 找断点账号 + 当前大循环/小轮
2. 算漏数:优先「待补漏」sheet,fallback 看 log 算 quota - 已成功
3. 环形重排:`items[idx:] + items[:idx]`
4. 写白名单 + 备份

**用户 3 步**:cd 件目录 → python3 catchup.py → 双击 go.command

诞生于 2026-05-02 04:09 电信断网事件(全队 394 个账号误判硬终止)。

## v1102(2026-05-04)主线内化中断恢复 — 取代独立脚本

**架构反转**:v1101.5 "主线零内部控制" 改为 **主线 gtg_batch / gtg_timer 自己内化中断恢复**,catchup.py 保留作 backup 不主推。

**核心机制**:
- 「本轮已发」 sheet 加 **「已发次数」列** (账号, count)
- sheet **不在小轮末 clear**,**累积到大循环末才 clear**(齐活才清)
- 每次成功发文 → sheet 该账号 count += 1
- 主线启动 → 读 sheet 重建 acc_count[账号] = count → 算 quota - count = 缺 N → 缺 0 跳过 / 缺 N>0 进 accounts_quota
- 主循环 acc_count < quota 自然停 = **不超不漏**

**业务语义(缺哥拍板 2026-05-04)**:
- 1 次发文 = 1 大循环 = N 小轮 (N = 素材数 // 账号数,动态算 — quota 不写死 5/3)
- 1 小轮 = 全账号各发 1 篇
- 中断在第 X 轮第 Y 账号 → 重启从该轮该账号继续:
  - 上面账号(< Y):已发 X 轮 = sheet count=X = 跳过
  - 中断点 + 下面(≥ Y):已发 X-1 轮 = sheet count=X-1 = 还差 1 篇
  - timer 排第 X 小轮:101 个账号(中断+下面),每号 1 篇
- "本轮不重发 + 缺 N 补 N" = 业务规则推出来 "从中断处起" 的最简方案

**修补关键**:batch.py 现有 `_clear_round_sheets()` 在小轮末调用 = bug,要移到大循环末

## v1102 用户主动重置出口(2026-05-04 缺哥拍板)

如果用户**不想从中断处接着跑**(比如换素材池 / 换发文计划 / 怀疑数据脏 / 想重新分配),**只需手动进 账号配置.xlsx 清空相关 sheet**:

- 「白名单」清空 → 主线动态从罐头侧边栏拿全账号
- 「本轮已发」清空 → acc_count 全 0 → 跑完整大循环 N 小轮
- 「待补漏」清空(可选)
- 「失败列表」清空(可选)
- 「硬终止账号」**保留**(被禁言/封号/失登的不应该重排,这条不该清)

主线启动 → 读 sheet 全空 → 自然进入"全新开跑"模式,无需改代码。

**Why**:用户在罐头侧手动清 = 最直接的 escape hatch,不依赖任何重置脚本。中断恢复是默认行为,但用户随时可以放弃。

## v1102 不动:
- 4 类硬终止 / 「硬终止账号」 sheet
- 「待补漏」 sheet (timer 退出时写,catchup backup 用)
- 「失败列表」 sheet + Phase B 轮末补发
- 「永久跳过」 sheet
- Phase A/B/C/D/E 死磕 / 篇间等待 / cliclick / 罐头侧边栏顺序

**实证(2026-05-04 NEO2 验证)**:
NEO2 当前轮 117 已发,关 timer + 注入 sheet (117 行 count=1) + 启 timer →
- 启动 log "本轮已发 117 篇,quota 部分扣 117 个,本轮还需排 333 篇"
- 排程 33 个 q=3 早窗 + 150 个 q≥2 中窗 + 150 个 q≥1 晚窗 = 333 任务
- 数学正确,不超 quota

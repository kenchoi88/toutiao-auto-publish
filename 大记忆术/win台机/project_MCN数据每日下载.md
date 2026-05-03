---
name: MCN 流量对比每日下载(Claude 接手)
description: 罐头 MCN 数据每天从 mp 后台拉小馆+迦境+收益,追加列到流量对比汇总.xlsx,2026-04-26 起从 Mac air 搬到 Win 台机由 Claude 接手
type: project
originSessionId: ed3bc523-a7f0-4efd-9774-5194c563ed34
---
**任务交接(2026-04-26):**
原本在 Mac air 桌面 MCN数据下载/ 跑(`go.command` 启 `data_pull.py`),现在搬到 Win 台机桌面 `C:\Users\kench\Desktop\MCN数据下载\`,**以后每天由 Claude 跑**(双击「下载.bat」)。

**Why:** 用户原话"以后由你接手每天下载"——这是一条**周期性任务的所有权转移**,不是一次性指令。

**How to apply:**
- 每天上午用户提"跑 MCN 数据下载"或类似时,直接 Bash 进 `C:\Users\kench\Desktop\MCN数据下载\` 跑 `python data_pull.py`(或加 `--today` 取当天实时)。
- 跑完检查输出:每个矩阵 sheet 应有「X号阅读/X号推荐」新列,收益 sheet 应补到 stat_date-1。
- 如果用户没主动提,我也可以在每天首次互动时**主动提醒**:"今天 MCN 数据下载跑了吗?"
- **常见报错处理**:
  - "cookie 没读到 sessionid" → 用户需在罐头里重新登录两个矩阵账号(小馆 7477169161966321683 / 迦境 7601367523329638450)
  - "找不到流量对比汇总.xlsx" → 用户没把文件拷过来,提醒他从 air 桌面拷
  - "中止:X号阅读列已有数据" → 防覆盖定格快照,如真要重跑需手动清空该列
- **路径关键差异(Mac vs Win)**:Win 上 Cookies 在 `Partitions\<id>\Network\Cookies`(多一层 Network),脚本已自适应。
- **不要在 Mac air 上再跑这个任务**(避免双跑覆盖)。流量对比汇总.xlsx 现在的"权威拷贝"在 Win 台机桌面。

**XLSX 结构提醒:**
- 多个 sheet:小馆-微头条 / 小馆-文章 / 迦境-微头条 / 迦境-文章 / 收益(小馆+迦境)
- 列名格式:"X月Y号"(发布日行) + "X号阅读/X号推荐"(统计日列)
- 防重复跑机制已经内置,不会一不小心覆盖

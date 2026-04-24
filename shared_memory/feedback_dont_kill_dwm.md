---
name: 不要 kill DWM（Win11 任务栏维修禁忌）
description: Win11 上 kill DWM 可能黑屏无法恢复、需强制重启，且重启后任务栏问题通常并未解决——这条路不要走
type: feedback
---
# 不要拿 "重启 DWM / kill 系统 shell 进程" 当任务栏修复手段（Win11）

## 规则
- **Win11 上禁止 kill dwm.exe**（无论提权与否），这不是"屏幕黑一瞬间"的小动作
- 对任务栏"失高亮 / 失 TOPMOST / z-order 错乱 / 亚克力失效 / 被窗口盖住"类问题，**不要**靠 kill 系统进程链（explorer → StartMenuExperienceHost → ShellExperienceHost → SearchHost → TextInputHost → dwm）去试错
- 这类做法既不能保证修好，副作用又可能是黑屏卡死需要强制关机重启

## Why
2026-04-24 台机 agent 崔巉为修"任务栏不高亮、所有窗口都排在任务栏前面"的问题，依次 kill 了：
1. explorer.exe —— 没效
2. StartMenuExperienceHost / ShellExperienceHost / SearchHost / TextInputHost —— 没效
3. 用 UAC 提权 kill dwm.exe —— **结果：整个屏幕黑屏无法恢复，缺哥被迫强制关机重启整机，重启后任务栏问题依然存在**

给缺哥的副作用预告是"屏幕黑一瞬间 <1 秒"——这是乐观估计、不是实测，严重低估了真实风险。缺哥原话："高你麻痹，直接黑屏无法恢复，还要重启，重启还没解决，操。"

## How to apply
- **不碰 DWM**：任何以"重启 DWM"为手段的方案，一票否决，不给用户当选项
- **任务栏亚克力 / 高亮 / topmost 异常**：先只读查配置（EnableTransparency / HighContrast / 电源计划 / TaskbarAl / TaskbarGlomLevel / StuckRects3），不要进入"逐个 kill shell 进程试错"模式
- **如果只读查配置全正常**：坦白告诉用户"配置层没问题，是运行时 bug，最稳方案是正常重启系统或注销再登入"，不要再自作聪明去 kill 系统进程
- **系统进程破坏性操作的副作用预告必须基于实测或官方文档**——禁止再用"闪一下""一瞬间""<1 秒"这种乐观用词；老老实实说"可能需要强制重启"才对得起用户
- 这条通用于所有 Win11 agent（台机崔巉 / mini 崔东山 / 未来云端 openclaw 等），不只本机

## 正确的修法
见 [feedback_taskbar_inactive_fix.md](feedback_taskbar_inactive_fix.md)：第一招按 **Win → Esc** 触发内置重绘，0 副作用。2026-04-24 缺哥这一按就把折腾半天都没修好的任务栏修好了。

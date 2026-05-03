---
name: 改 HKCU 注册表不需要管理员
description: 清系统代理可以不走 UAC——HKCU 是当前用户的注册表，普通权限能写
type: feedback
originSessionId: 5b0a52f9-fbb7-461f-8c1d-c85a747257a3
---
Windows 上清系统代理（ProxyEnable / ProxyServer / AutoConfigURL）的 reg add 指向 `HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings`，**普通用户权限直接能写**，不要画蛇添足加 UAC 提权。

**Why:** UAC 弹窗是缺哥台机上脚本闪退的元凶：启动器→PowerShell Start-Process -Verb RunAs→弹 UAC→失败/拒绝，窗口瞬间关，看都看不见。2026-04-20 缺哥因此骂了我一顿。

**How to apply:**
- 只改 HKCU 的 bat：**不加 UAC**，双击就跑，pause >nul 收尾
- 杀 v2rayN.exe / xray.exe 才需要 admin（如果 V2 以管理员运行），但这一步**交给缺哥自己右键托盘退出**，agent 不碰（见 feedback_dont_kill_v2）
- 反面教材：不要搞 launcher.bat + worker.bat + VBS 这种嵌套提权，一层错层层崩

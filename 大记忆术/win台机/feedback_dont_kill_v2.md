---
name: 别自己关 V2
description: agent 自己结掉 v2rayN/xray 进程 = 立刻断掉自己跟 Anthropic 的连接，后续无法工作
type: feedback
originSessionId: 5b0a52f9-fbb7-461f-8c1d-c85a747257a3
---
不要用 taskkill / Stop-Process 杀 v2rayN.exe 或 xray.exe。

**Why:** 缺哥台机的 VS Code 走 `http.proxy=socks5://127.0.0.1:10808` 连 Anthropic API。10808 是 xray 监听的。xray 一死，我跟缺哥之间的通道就断，正在进行的任务当场失联，缺哥还要自己手动重开 V2 才能回来继续对话。2026-04-20 已经因此挨过一次骂。

**How to apply:**
- 验证 / 诊断代理问题时：只读（Get-Process、netstat、reg query），不动进程
- 脚本要杀 V2 是可以写的，但**让缺哥自己双击**执行，agent 端绝不直接 Invoke
- 桌面 `清理代理.bat` 是给缺哥用的，不是给我用的
- 如果必须改 V2 状态（比如改 config），优先用"改文件+提示缺哥重启 V2"，不要靠杀进程触发

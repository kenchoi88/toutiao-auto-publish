---
name: 跨机 ssh 启脚本必须 login shell
description: ssh 远程起 python / 脚本一律 bash -lc / zsh -lc 或显式 PATH;不许裸 ssh 起 — non-interactive PATH 不含 brew 工具,subprocess 调 cliclick 等会炸,且无声白跑
type: feedback
originSessionId: b5e5a8ce-2387-44d4-9851-658903ac1976
---
凡 ssh 远程启动 python / 发文脚本,命令一律 `bash -lc '...'` 或 `zsh -lc '...'`,或显式 `PATH=/usr/local/bin:/opt/homebrew/bin:$PATH python3 ...`。**不许裸** `ssh user@host "cd ... && python3 ..."`。

**Why:** 2026-05-05 NEO 5h 白跑事故 — 另一窗口绣虎用 `ssh kenchoios@... "cd && python3 gtg_timer.py &"` non-interactive 起 gtg_timer。Non-interactive shell 不加载 ~/.zshrc,Python 进程继承默认 PATH(/usr/bin:/bin:/usr/sbin:/sbin),不含 /usr/local/bin、/opt/homebrew/bin → brew 装的 **cliclick 找不到** → subprocess 报 `No such file or directory: 'cliclick'` → 文档回池尾重试 → 5h 跑了 512 次全失败 0 publish,缺哥还以为在正常发文,浪费几小时 + 挨揍。

**How to apply:**
1. 远程启动发文脚本 → `ssh user@host "bash -lc 'cd ... && python3 gtg_timer.py'"`(login shell 完整 PATH)
2. 后台脱终端 → `ssh user@host "bash -lc 'cd ... && nohup python3 gtg_timer.py > /dev/null 2>&1 &'"`
3. 或 显式 PATH:`ssh user@host "cd ... && PATH=/usr/local/bin:/opt/homebrew/bin:\$PATH nohup python3 gtg_timer.py &"`
4. 启完必须实证:`ssh user@host "tail 运行日志.txt"` 看到正常 publish 流不报 `No such file or directory: 'cliclick'`,才算启对
5. `go.command` 双击 OK — 走 Terminal login shell,PATH 完整(但 ssh 远程不能双击,所以必须自己保证 login shell)
6. 远程**只读**命令(ls/ps/cat/grep/wc)不强制 login shell;但任何会触发 subprocess 调外部工具(cliclick / brew 装的 git / open / osascript / pyautogui 系)的命令必须走 login shell
7. 启动后 30 秒内必看 log,确认无 PATH 类错误(找不到命令 / No such file or directory),不闷头跑

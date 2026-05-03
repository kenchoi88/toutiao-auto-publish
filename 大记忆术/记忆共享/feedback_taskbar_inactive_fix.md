---
name: Win11 任务栏"失活卡态"的正确修法
description: 任务栏发灰、失高亮、图标下无运行横线、看似被窗口盖住——先 Win 键再 Esc，不要 kill 进程链
type: feedback
---
# Win11 任务栏"失活卡态"——先 Win+Esc，再考虑别的

## 规则
碰到任意一种或多种症状：
- 任务栏发**灰色**、丢了壁纸透出的亚克力/透明效果
- 图标下面**没有蓝色"运行中"横线**
- 直观看上去**所有窗口都排在任务栏前面**（但任务栏其实没被遮）
- 重启系统**没有解决**

**第一招永远先试：按一下 Win 键（打开开始菜单）→ 按 Esc 关掉。**

这个动作 0 副作用、是 Windows 原生刷新路径，大多数"失活卡态"会被它触发重绘恢复。

## Why
2026-04-24 台机崔巉为修缺哥台机的任务栏失高亮问题，走歪路一路 kill：
1. explorer → 没效
2. StartMenuExperienceHost / ShellExperienceHost / SearchHost / TextInputHost → 没效
3. UAC 提权 kill DWM → **整机黑屏强制重启**
4. 重启后问题依然——因为根因跟 DWM/shell 进程无关

最后换方向查：用 `GetTopWindow` + `GetWindow(GW_HWNDNEXT)` 枚举 z-order 从顶到 Shell_TrayWnd 之间的所有可见窗口，结果发现 **没有任何可见窗口真的压在任务栏上**——根因是任务栏**自己卡在"失活视觉态"**，不是被遮挡。

最后缺哥按 Win 再按 Esc，状态立刻恢复。

## How to apply
- **按症状先判断**：如果任务栏"看似被盖"但 z-order 枚举显示其实没人压，就是这个 bug
- **第一招**：让用户按 Win → Esc。**不要自己用 SendKeys 发**（焦点可能在输入框，误伤）
- **如果 Win+Esc 不好使**，再按风险从小到大往后试：
  1. 用户在任务栏空白处右键→关菜单（触发重绘）
  2. 用户切换任务栏对齐方式（设置→个性化→任务栏，居中↔靠左）
  3. 改注册表 `HKCU:\...\Explorer\Advanced\TaskbarAl` 0↔1 并重启 explorer
  4. 显卡驱动更新（NVIDIA/AMD 都有过 Win11 任务栏渲染相关 bug）
  5. Windows 累积更新到最新
- **永远不要走**：kill explorer/StartMenuExperienceHost/ShellExperienceHost/SearchHost/**dwm** 这条链（详见 `feedback_dont_kill_dwm.md`）
- **查 z-order 的正确工具代码**（PowerShell 变量名避开 `$PID` 保留字）：
  ```powershell
  # 枚举 z-order 找真正在任务栏之上的可见窗口
  # 用 GetTopWindow + GetWindow(GW_HWNDNEXT=2) 迭代到 Shell_TrayWnd
  # 每个窗口查 IsWindowVisible + GetWindowLong(GWL_EXSTYLE) & WS_EX_TOPMOST(0x8)
  # 变量名用 $procId 不要 $pid
  ```

通用于所有 Win11 agent。

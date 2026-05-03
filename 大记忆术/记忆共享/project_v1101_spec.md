---
name: v1101 大统一 spec(2026-04-28)
description: 三大件 v1101 基线 + 必含 patches + per 大件 base 选择;改前必读,改后核对完成度
type: project
---

## 命名约定
- v1101 = 今天(2026-04-28)统一基线
- 后续我每改一次 → 新建 `XXX自动发布101.1版/`,`101.2版/` 文件夹,旧版保留
- 仓库目录:`自动发布/{微头条自动发布101版,文章自动发布101版,文章定时自动发布101版}/{mac,win}/`(待建)

## 大件代号
- **微头条自动发布**(简称 微头条)
- **文章自动发布**(简称 文章)
- **文章定时自动发布**(简称 文章定时)

## Base 选择

| 大件 | base 来源 | 字节 | 选择理由 |
|---|---|---|---|
| 微头条 | win 桌面 gtg_batch.py | 83610 | 搜索框 8 处最深,阅读量 12 处最全 |
| 文章 | win 桌面 gtg_batch.py | 86260 | 搜索框 8 处最深,体量最大 feature 最全 |
| 文章定时 | mini 桌面 gtg_timer.py | 78963 | 含定时排程核心 + 罐头自愈 + 熔断 + DIAG patch |

## v1101 必含 patches(三大件全要)

### P1 — 删 Step 3 主对话框 6s 硬等
- 位置:fill_dialog 内 Step 3 自动关检测的 12×0.5s loop
- 改动:整段删除,直接进 Step 4 cliclick 点"打开"按钮兜底
- 理由:macOS 26 NSOpenPanel 行为变了,Step 3 必满 6s 纯发呆

### P2 — 字数 < 50 → 重试 fill_dialog 一次
- 位置:对话框关闭后 char_count 检测之后
- 改动:char_count < 50 时,重新触发 fill_dialog + 再读字数,仍 < 50 才 return False
- 理由:对话框关了但 docx 没真导入是常态(夜间高发),救一半冤枉报废

### P3 — ProseMirror 选择器改为取最长元素
- 位置:char_count 读取的 JS
- 改动:`document.querySelector('.ProseMirror')` → `Array.from(querySelectorAll('.ProseMirror'))` 取最长 textContent
- 理由:首个 ProseMirror = 标题输入框 placeholder "请输入标题" 5 字,正文 ProseMirror 在第二位被忽略,4 天 273 次冤杀

### P4 — [DIAG] 确认发布按钮 DOM dump(只 文章 + 文章定时,微头条无确认弹窗)
- 位置:"确认发布未出现"前
- 改动:dump 所有 button textContent + 含"发布"字非 button 可见叶子,写 [DIAG] log
- 理由:JS 选择器漏匹配是常态,需 DOM 数据改选择器

### P5 — ensure_gtg_top 强化
- 位置:ensure_gtg_top 函数
- 改动:加 `set visible to true`(处理 Cmd-H Hidden) + `perform action "AXRaise"`(强制 reorder) + verify `frontmost`(失败重试 3 次)
- 理由:罐头被推后台 → cliclick 命中错对象 → publish 失败的隐性来源

### P6 — Win 飘屏外坐标兜底(仅 win 三大件)
- 位置:任何算 webview 屏幕坐标后
- 改动:坐标为负 → Win32 `SetWindowPos` 拉回(100, 100) → 再读
- 理由:win 定时 04-28 01:53-09:08 飘屏外 7 小时 85 次失败的根因

### P7 — cliclick 重试(三大件全)
- 位置:每次 cliclick 之后等弹窗 / 状态变化的 poll
- 改动:30s timeout 内 弹窗未出 → 重读按钮坐标 + ensure_gtg_top + 再 cliclick(共 2-3 次)再判失败
- 理由:Mac 散点 cliclick 不响应 4 天 77 次,加重试救大半

### P8 — 抄搜索框 fallback(全队 文章定时 必含,非可选)
- 位置:scroll_find_account / find_account_webview
- 改动:把 win 的 `find_or_reopen_webview` + `_search_box_set` + 搜索框过滤 移植到 mac gtg_timer.py
- 理由:mac 文章定时全无搜索框,底部账号 webview partition 挂 → 死循环 N 圈无救

### P9 — 抄 win 阅读量回查(只 mac 文章定时)
- 位置:发文成功后,关 tab 前
- 改动:抄 win 的"阅读量: [N, N, N]" 检测
- 理由:mac 文章定时 0 处阅读量回查,缺监控信号

### P10 — Stage 2 死磕加熔断(只 文章定时)
- 位置:Stage 2 死磕主循环
- 改动:抄 Stage 1 的 `consecutive_fail >= MAX_CONSECUTIVE_FAIL → break + 系统通知`
- 理由:Stage 2 缺熔断,罐头死/网络断/飘屏外 → 死磕几小时无人救

## 不入 v1101 的(单独处理)

- **#2 neo SSH 不通**:配置/网络问题,跟代码 v1101 无关。修法:GUI 开 Remote Login / 开 Tailscale SSH tag

## 完成度核对表(每脚本逐项)

| 大件 | base | P1 | P2 | P3 | P4 | P5 | P6(Win 限) | P7 | P8 | P9 | P10 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 微头条 v1101 | win | ✅ | ✅ | ✅ | N/A | ✅ | ✅(win) | ✅ | N/A | N/A | N/A |
| 文章 v1101 | win | ✅ | ✅ | ✅ | ✅ | ✅ | ✅(win) | ✅ | N/A | N/A | N/A |
| 文章定时 v1101 | mini | ✅ | ✅ | ✅ | ✅ | ✅ | ✅(win) | ✅ | ✅ | ✅ | ✅ |

(全 ✅ 才算 v1101 完成)

## 落地顺序

1. 先合 v1101 三个 .py 文件(草稿在仓库 `自动发布/XXX自动发布101版/{mac,win}/`)
2. py_compile 通过
3. 各机当前批跑完后,scp 桌面真版 + 备份原文件
4. 重启对应脚本,monitor 1 小时验证
5. 完成度核对表全 ✅ → 章程 + memory 更新

## Why
2026-04-28 缺哥拍 — 之前不停"补漏"模式,改一处漏一处,版本永远不齐。从今天起以 v1101 为统一基线,所有机所有大件对齐这份 spec,改完核对表标 ✅ 才算完。

## How to apply
- 改任何脚本前先读这份 spec
- 改完逐项核对完成度表
- 章程(`project_claude_分工章程.md`)+ 这份 spec 是各机 Claude 的 north star

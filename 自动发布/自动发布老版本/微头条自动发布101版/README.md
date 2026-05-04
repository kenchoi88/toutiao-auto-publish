# 微头条自动发布 v1101

**统一基线版本**(2026-04-28 起)

## 目录
- `mac/` — Mac 端 Python + .command 启动器
- `win/` — Win 端 Python + .bat 启动器

## 落地

各机 `git pull` → cp 对应 OS 子目录的脚本到自己桌面真版位置 → 重启脚本。

**不会覆盖各机本地数据**(账号配置.xlsx / 素材/ / 运行报告/ — 由 .gitignore 排除)。

## v1101 含 Patches(详见 [shared_memory/project_v1101_spec.md](../../shared_memory/project_v1101_spec.md))

| Patch | 含 |
|---|---|
| P1 | 删 Step 3 6s 硬等(macOS 26 NSOpenPanel 自动关失效) |
| P2 | 字数<50 重试 fill_dialog 一次 |
| P3 | ProseMirror 选择器取最长元素(避免命中标题 placeholder 5 字) |
| P5 | ensure_gtg_top 强化(unhide + AXRaise + verify frontmost + 重试 3 次) |
| P7 | cliclick 重试 3 次(配合重 activate + 重读坐标) |
| (DIAG) | 文章定时:抓"确认发布"按钮 DOM dump |

## 待落地(v1101.1)
- P8 抄 win 8 处搜索框 fallback(只 mac 文章定时)
- P9 抄 win 阅读量回查(只 mac 文章定时)
- P10 Stage 2 死磕加熔断(只 文章定时)
- P4 [DIAG] 微头条 + 文章 也补
- P6 Win 飘屏外坐标兜底(只 win)

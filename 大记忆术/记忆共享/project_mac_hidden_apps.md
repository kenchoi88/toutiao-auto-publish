---
name: neo的Mac隐藏应用（防儿子偷玩）
description: 缺哥儿子来访前neo上藏起来的应用，用完要搬回来
type: project
originSessionId: 6d1e89eb-eddc-422c-b35c-b420271a3a68
---
**藏在 `~/.hidden_apps/` 里的应用（neo机器上）：**
- `WeChat.app`
- `Google Chrome.app`
- `哔哩哔哩.app`

**其他操作：**
- 苹果账号已退出（App Store无法下载）
- TikTok是网页版，没有独立app，藏不了

**还原命令（儿子走后在neo上执行）：**
```bash
sudo mv ~/.hidden_apps/WeChat.app /Applications/
sudo mv ~/.hidden_apps/Google\ Chrome.app /Applications/
sudo mv ~/.hidden_apps/哔哩哔哩.app /Applications/
```

**Why:** 2026-03-29儿子（高一）来访，怕他偷玩不学习
**How to apply:** 儿子走了缺哥会喊，SSH进neo执行还原命令，再提醒他重新登录苹果账号

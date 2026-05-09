---
name: 罐头下载弹窗消除方案 (Page.setDownloadBehavior + Fetch + requests)
description: 罐头 Electron 强制弹"另存为"无法用 Browser.setDownloadBehavior 关掉,组合 Page-level + Fetch 拦截 + requests 直拉绕过
type: reference
originSessionId: 65e7943b-4b50-4d8f-8d15-a85ca3997cff
---
罐头(Electron app v1.7.11) 触发下载会强制弹 Windows 11 "另存为"对话框,Chromium flag (`--disable-features=DownloadBubble`) 让罐头闪退,Browser.setDownloadBehavior 单独不生效,守护按 Enter 拦不到(对话框 title 是 URL,EnumWindows #32770 时序问题)。

实证 2026-05-09 work 的组合方案 (在 罐头爆款下载.py click 下载按钮前):

1. **Page.setDownloadBehavior 'allow' + downloadPath** (page-level,不是 browser-level)
2. **Fetch.enable** patterns=`[{'urlPattern': '*muse-file-sign*', 'requestStage': 'Request'}]`
3. click 下载按钮 (CDP mouseEvent + .click() 兜底)
4. ws 监听 `Fetch.requestPaused` event,匹配 muse-file-sign URL → `Fetch.failRequest` errorReason='Aborted' (cancel 浏览器下载,无弹窗)
5. Python `requests.get(captured_url, timeout=60)` 直拉 (签名 URL 自带 x-signature/x-expires,**不需 cookies/headers**)
6. 写到 WATCH_DIR (脚本后续监听逻辑兼容)

避坑:
- `Browser.setDownloadBehavior` 单独用不行,要 `Page.setDownloadBehavior` page-level
- `Fetch.failRequest` 在 Request 阶段 cancel 才不弹,Response 阶段晚了
- requests 不要传 captured_headers (含中文 referer 触发 latin-1 codec error)
- ws.settimeout 用完必须复位 None,否则后续 cdp() 调用超时
- 罐头进程名是 `创作罐头.exe` (debug_launch.py 原本对),`DS创作V1.1.0.exe` 是另一个 App (DS 创作洗稿工具),别杀错

#!/bin/bash
# v1101.3 守护脚本 (Mac 端) — 防 Finder 兜底抢前台
#
# 现象:gtg_batch.py 跑发文时,篇间等待 8~17 秒期间罐头失去 frontmost,
#       mac 系统默认把 frontmost 给 Finder → 桌面壁纸冒出来,看上去
#       窗口"忽然消失";下篇开始时 ensure_gtg_top 才把罐头拉回来,
#       视觉上反复"切 App"。
#
# 修法:后台 0.5s 轮询 frontmost,只在 frontmost=Finder 时介入,
#       立即 activate 创作罐头。其他 App frontmost(脚本 cliclick / 系统
#       对话框)一概不动,无副作用。
#
# 启动:bash keep_canned_top.sh   (建议 nohup ... &  后台跑)
# 停止:pkill -f keep_canned_top
#
# 部署机:air / neo / neo2 / mini  四台 Mac 通用

while true; do
    front=$(osascript -e 'tell application "System Events" to get name of first application process whose frontmost is true' 2>/dev/null)
    if [ "$front" = "Finder" ]; then
        osascript -e 'tell application "创作罐头" to activate' 2>/dev/null
    fi
    sleep 0.5
done

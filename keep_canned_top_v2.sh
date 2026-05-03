#!/bin/bash
# keep_canned_top_v2.sh — 5 机统一(AIR/NEO/NEO2/MINI 用)
# 罐头不在前台 + frontmost 不在白名单 → activate 罐头
# 白名单(缺哥 2026-05-03 拍):VS Code / 微信 / 访达 / Tailscale / Shadowrocket(+ 罐头自身)
# 防抖:连续 N 次命中条件才触发 activate,防止 frontmost 短暂闪 Finder 时误抢

CANNED_KEYWORD="创作罐头"   # 罐头窗口标题/进程名包含此关键词
SCRIPT_NAME="gtg_batch\|gtg_timer"   # 只在发文期生效

# 白名单 — frontmost app name 在内则不抢
WHITELIST=(
  "Code"           # VS Code
  "Cursor"         # 备:小齐若是 Cursor
  "WeChat"         # 微信
  "Finder"         # 访达 — 缺哥首要
  "Tailscale"      # Tailscale
  "Shadowrocket"   # 小火箭
  "创作罐头"        # 罐头自身已 frontmost 不需 activate
  "Terminal"       # 命令行
  "iTerm2"
)

DEBOUNCE=3       # 连续 N 次都判定"该抢"才真抢,防短暂闪烁
SLEEP=1          # 轮询间隔(s)

ACTIVATE_OSA='tell application "'"$CANNED_KEYWORD"'" to activate'

frontmost_name() {
  osascript -e 'tell application "System Events" to get name of first process whose frontmost is true' 2>/dev/null
}

is_whitelisted() {
  local name="$1"
  for w in "${WHITELIST[@]}"; do
    if [[ "$name" == *"$w"* ]]; then return 0; fi
  done
  return 1
}

script_running() {
  pgrep -f "$SCRIPT_NAME" >/dev/null
}

LOG=~/keep_canned_top.log
echo "[$(date '+%Y-%m-%d %H:%M:%S')] keep_canned_top_v2 启动 PID=$$" >> "$LOG"

count=0
while true; do
  if ! script_running; then
    count=0
    sleep $SLEEP
    continue
  fi
  fg=$(frontmost_name)
  if is_whitelisted "$fg"; then
    count=0
  else
    count=$((count + 1))
    if [ $count -ge $DEBOUNCE ]; then
      osascript -e "$ACTIVATE_OSA" 2>/dev/null
      echo "[$(date '+%Y-%m-%d %H:%M:%S')] 抢回罐头 (frontmost=$fg)" >> "$LOG"
      count=0
    fi
  fi
  sleep $SLEEP
done

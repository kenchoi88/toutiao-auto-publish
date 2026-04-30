#!/bin/bash
# frontmost App 追踪 (纯观察 / 不动任何 App / 不改行为)
# 用法:nohup ~/frontmost_trace.sh > ~/frontmost_trace.log 2>&1 & disown
# 停:pkill -f frontmost_trace
while true; do
  ts=$(date '+%Y-%m-%d %H:%M:%S')
  front=$(osascript -e 'tell application "System Events" to get name of first application process whose frontmost is true' 2>/dev/null)
  echo "$ts $front"
  sleep 0.5
done

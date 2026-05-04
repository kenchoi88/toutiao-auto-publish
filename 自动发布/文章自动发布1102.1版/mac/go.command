#!/bin/bash
DIR="$(cd "$(dirname "$0")"; pwd)"
osascript <<EOF
tell application "Terminal"
    activate
    do script "cd '$DIR' && python3 gtg_batch.py"
end tell
EOF

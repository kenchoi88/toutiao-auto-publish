#!/bin/bash
DIR="$HOME/Desktop/文章定时自动发布"
osascript -e "tell application \"Terminal\" to do script \"sleep 5 && tail -f '$DIR/运行报告/$(date +%Y%m%d)/运行日志.txt'\""
cd "$DIR" && /usr/bin/python3 gtg_timer.py

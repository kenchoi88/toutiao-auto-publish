#!/bin/bash
DIR="$HOME/Desktop/Mac文章自动发布"
osascript -e "tell application \"Terminal\" to do script \"sleep 5 && tail -f '$DIR/运行报告/$(date +%Y%m%d)/运行日志.txt'\""
cd "$DIR" && python3 gtg_batch.py

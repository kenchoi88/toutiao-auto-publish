#!/bin/bash
cd "$(dirname "$0")"
python3 data_pull.py
echo ""
echo "按任意键关闭..."
read -n 1

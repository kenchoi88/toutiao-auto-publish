@echo off
chcp 65001 >nul
cd /d %~dp0
python gtg_timer.py 2>&1
pause

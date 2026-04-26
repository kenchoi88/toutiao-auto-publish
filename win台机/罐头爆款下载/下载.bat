@echo off
chcp 65001 >nul
cd /d %~dp0
echo === 罐头爆款下载 ===
echo.
echo 前提:罐头已用 debug_launch.bat 启动到 CDP 9223
echo.
python "罐头爆款下载.py"
echo.
pause

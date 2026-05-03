@echo off
chcp 65001 > nul
cd /d "%~dp0"
python data_pull.py %*
echo.
echo 按任意键关闭...
pause > nul

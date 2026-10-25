@echo off
title 美少女图鉴服务器
cd /d "%~dp0"
echo 正在启动美少女图鉴服务器（关闭此窗口即停止服务）...
python server.py
echo.
echo 服务器已退出。
pause

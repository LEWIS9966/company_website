@echo off
chcp 65001 >nul
echo ========================================
echo 企业展示网站服务器
echo ========================================
echo.
echo 正在启动服务器...
echo.
echo 服务器启动后，请在浏览器中访问：
echo http://localhost:5000
echo.
echo 按 Ctrl+C 可以停止服务器
echo ========================================
echo.

cd /d "%~dp0"
py app.py

pause


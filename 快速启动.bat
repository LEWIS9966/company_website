@echo off
title 企业展示网站服务器
color 0A
chcp 65001 >nul
cls

echo.
echo ╔═══════════════════════════════════════════════════════╗
echo ║           企业展示网站服务器 - 启动中...              ║
echo ╚═══════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

echo [1/3] 检查Python环境...
py --version >nul 2>&1
if errorlevel 1 (
    echo     ✗ Python未找到，请先安装Python
    pause
    exit /b 1
)
echo     ✓ Python环境正常
echo.

echo [2/3] 检查依赖包...
py -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo     ✗ Flask未安装，正在安装...
    pip install -r requirements_website.txt
    if errorlevel 1 (
        echo     ✗ 依赖安装失败
        pause
        exit /b 1
    )
)
echo     ✓ 依赖包检查完成
echo.

echo [3/3] 启动服务器...
echo.
echo ═══════════════════════════════════════════════════════
echo   服务器启动后，请在浏览器中访问：
echo   http://localhost:5000
echo   或
echo   http://127.0.0.1:5000
echo ═══════════════════════════════════════════════════════
echo.
echo   按 Ctrl+C 可以停止服务器
echo.

timeout /t 2 /nobreak >nul

py app.py

echo.
echo 服务器已停止
pause


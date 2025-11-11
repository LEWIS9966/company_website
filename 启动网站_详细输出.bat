@echo off
chcp 65001 >nul
echo ========================================
echo 企业展示网站服务器（详细输出模式）
echo ========================================
echo.

cd /d "%~dp0"

echo 当前目录: %CD%
echo.
echo 检查Python...
py --version
echo.
echo 检查依赖...
py -c "import flask; print('Flask版本:', flask.__version__)" 2>nul || echo 错误: Flask未安装
echo.
echo 启动服务器...
echo ========================================
echo.

py app.py

echo.
echo ========================================
echo 服务器已停止
pause


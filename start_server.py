#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
启动服务器脚本
"""
import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app import app
    print("=" * 50)
    print("企业展示网站服务器启动中...")
    print("=" * 50)
    print("\n访问地址: http://localhost:5000")
    print("按 Ctrl+C 停止服务器\n")
    print("=" * 50)
    app.run(debug=True, host='127.0.0.1', port=5000, use_reloader=False)
except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()
    input("按回车键退出...")


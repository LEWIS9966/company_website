#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试服务器启动
"""
import sys
import os

print("测试1: 导入Flask...")
try:
    from flask import Flask
    print("✓ Flask导入成功")
except Exception as e:
    print(f"✗ Flask导入失败: {e}")
    sys.exit(1)

print("\n测试2: 创建Flask应用...")
try:
    app = Flask(__name__, 
                template_folder='templates',
                static_folder='static')
    print("✓ Flask应用创建成功")
except Exception as e:
    print(f"✗ Flask应用创建失败: {e}")
    sys.exit(1)

print("\n测试3: 检查模板目录...")
templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
if os.path.exists(templates_dir):
    print(f"✓ 模板目录存在: {templates_dir}")
    files = os.listdir(templates_dir)
    print(f"  模板文件: {', '.join(files)}")
else:
    print(f"✗ 模板目录不存在: {templates_dir}")

print("\n测试4: 检查静态文件目录...")
static_dir = os.path.join(os.path.dirname(__file__), 'static')
if os.path.exists(static_dir):
    print(f"✓ 静态文件目录存在: {static_dir}")
else:
    print(f"✗ 静态文件目录不存在: {static_dir}")

print("\n测试5: 添加测试路由...")
@app.route('/test')
def test():
    return '<h1>服务器运行正常!</h1><p>如果你看到这条消息，说明服务器已经成功启动。</p>'

print("\n测试6: 启动服务器...")
print("=" * 60)
print("服务器启动中，请访问: http://127.0.0.1:5000/test")
print("按 Ctrl+C 停止服务器")
print("=" * 60)

try:
    app.run(debug=True, host='127.0.0.1', port=5000, use_reloader=False)
except KeyboardInterrupt:
    print("\n服务器已停止")
except Exception as e:
    print(f"\n服务器启动失败: {e}")
    import traceback
    traceback.print_exc()


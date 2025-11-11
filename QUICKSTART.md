# 快速启动指南

## 第一步：安装依赖

```bash
pip install -r requirements_website.txt
```

## 第二步：运行应用

### Windows:
```bash
run.bat
```

### Linux/Mac:
```bash
chmod +x run.sh
./run.sh
```

### 或直接运行:
```bash
python app.py
```

## 第三步：访问网站

打开浏览器访问：http://localhost:5000

## 主要页面

- **首页**: http://localhost:5000
- **产品中心**: http://localhost:5000/products
- **公司简介**: http://localhost:5000/about
- **联系我们**: http://localhost:5000/contact
- **管理后台**: http://localhost:5000/admin

## 测试联系表单

1. 访问 http://localhost:5000/contact
2. 填写表单并提交
3. 访问 http://localhost:5000/admin 查看提交的数据

## 自定义配置

### 修改公司信息

编辑以下文件：
- `templates/base.html` - 页脚信息
- `templates/index.html` - 首页内容
- `templates/about.html` - 公司简介
- `templates/contact.html` - 联系方式

### 修改颜色主题

编辑 `static/css/style.css` 文件中的 CSS 变量（:root 部分）

### 添加图片

将图片放入 `static/images/` 目录：
- 产品图片: product1.jpg, product2.jpg, product3.jpg, product4.jpg
- 团队照片: team1.jpg, team2.jpg, team3.jpg
- 二维码: qrcode.png

## 数据库

数据库文件 `contacts.db` 会在首次运行时自动创建。

查看数据：
- 通过管理后台: http://localhost:5000/admin
- 或使用API: http://localhost:5000/api/contacts

## 常见问题

### 端口被占用

修改 `app.py` 最后一行的端口号：
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### 数据库问题

删除 `contacts.db` 文件，重新运行应用即可重建数据库。

## 下一步

- 添加真实的产品图片和团队照片
- 修改公司信息和联系方式
- 自定义颜色主题
- 配置生产环境部署


# 企业展示网站

一个现代化的企业展示型网站，用于对外展示公司产品、企业背景及联系方式。支持 Vercel 一键部署。

## 功能特性

- ✅ 响应式设计，支持PC端、平板和手机端
- ✅ 简洁专业的UI设计
- ✅ 产品展示页面，支持网格布局
- ✅ 公司简介页面，包含发展历程、团队介绍等
- ✅ 联系表单，支持数据提交和验证
- ✅ 后端API，数据存储到数据库
- ✅ 前端表单验证
- ✅ 数据库查询功能（支持按时间、联系方式、关键词查询）
- ✅ 支持 Vercel 部署

## 快速开始

### 本地开发

1. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

2. **配置环境变量**
   ```bash
   cp .env.example .env
   # 编辑 .env 文件，配置数据库连接
   ```

3. **运行应用**
   ```bash
   python app.py
   ```

4. **访问网站**
   - 打开浏览器访问: http://localhost:5000

### Vercel 部署

详细部署指南请查看 [VERCEL_DEPLOY.md](./VERCEL_DEPLOY.md)

#### 快速部署步骤

1. **准备 Git 仓库**
   - 将项目推送到 GitHub/GitLab/Bitbucket

2. **在 Vercel 上部署**
   - 登录 https://vercel.com
   - 点击 "Add New Project"
   - 选择你的 Git 仓库
   - 配置环境变量（DATABASE_URL, SECRET_KEY）
   - 点击 "Deploy"

3. **配置数据库**
   - 在 Vercel 项目设置中添加 Postgres 数据库
   - 或配置外部数据库连接字符串

## 项目结构

```
company_website/
├── api/
│   └── index.py          # Vercel Serverless Function入口
├── templates/             # HTML模板
│   ├── base.html         # 基础模板
│   ├── index.html        # 首页
│   ├── about.html        # 公司简介
│   ├── contact.html      # 联系我们
│   ├── products.html     # 产品中心
│   └── admin.html        # 管理后台
├── static/               # 静态资源
│   ├── css/
│   │   └── style.css     # 样式文件
│   ├── js/
│   │   ├── main.js       # 主JavaScript文件
│   │   └── contact.js    # 联系表单处理
│   └── images/           # 图片资源
├── requirements.txt      # Python依赖
├── vercel.json          # Vercel配置
├── .vercelignore        # Vercel忽略文件
├── .env.example         # 环境变量示例
├── app.py               # 本地开发服务器（可选）
└── README.md            # 项目说明
```

## 数据库

### 本地开发

可以使用 SQLite（修改 `app.py` 中的数据库配置）或 PostgreSQL。

### 生产环境（Vercel）

**推荐使用 Vercel Postgres**：
1. 在 Vercel 项目设置中添加 Postgres 数据库
2. Vercel 会自动提供 `POSTGRES_URL` 环境变量
3. 应用会自动使用该数据库

**或使用外部数据库**：
- Supabase
- PlanetScale
- Railway
- 其他 PostgreSQL 兼容数据库

### 数据模型

- `id`: 主键
- `name`: 客户称呼
- `gender`: 性别（男/女/其他）
- `phone`: 手机号
- `email`: 邮箱
- `requirements`: 具体需求
- `submit_time`: 提交时间

## API接口

### 1. 提交联系表单
- **URL**: `/api/submit-contact`
- **方法**: POST
- **请求体**: JSON
  ```json
  {
    "name": "客户称呼",
    "gender": "男/女/其他",
    "phone": "手机号",
    "email": "邮箱",
    "requirements": "具体需求"
  }
  ```
- **响应**: JSON
  ```json
  {
    "success": true/false,
    "message": "提示信息"
  }
  ```

### 2. 查询联系表单数据
- **URL**: `/api/contacts`
- **方法**: GET
- **查询参数**:
  - `page`: 页码（默认1）
  - `per_page`: 每页数量（默认20）
  - `search`: 搜索关键词
  - `sort_by`: 排序字段（submit_time/name）
- **响应**: JSON
  ```json
  {
    "success": true,
    "data": [...],
    "total": 总记录数,
    "page": 当前页码,
    "per_page": 每页数量,
    "pages": 总页数
  }
  ```

## 页面说明

### 首页
- 公司主营业务展示
- 产品展示区域
- 公司亮点统计

### 产品中心
- 产品列表展示
- 产品详情和特点
- 咨询按钮

### 公司简介
- 公司概述
- 发展历程时间线
- 核心团队介绍
- 价值观与使命
- 荣誉资质

### 联系我们
- 联系方式展示
- 联系表单
- 表单验证
- 提交成功提示

### 管理后台
- 联系表单数据查看
- 搜索功能
- 排序功能
- 分页显示
- 统计信息

## 环境变量

| 变量名 | 说明 | 必需 | 示例 |
|--------|------|------|------|
| `DATABASE_URL` | 数据库连接字符串 | 是 | `postgresql://user:pass@host/db` |
| `POSTGRES_URL` | Vercel Postgres连接字符串 | 否 | 自动提供 |
| `SECRET_KEY` | Flask会话密钥 | 是 | `your-secret-key` |

## 自定义配置

### 修改公司信息

编辑 `templates/` 目录下的HTML文件：
- `base.html` - 页脚信息
- `index.html` - 首页内容
- `about.html` - 公司简介
- `contact.html` - 联系方式

### 修改颜色主题

编辑 `static/css/style.css` 中的CSS变量：
```css
:root {
    --primary-color: #2563eb;    /* 主色调 */
    --primary-dark: #1e40af;     /* 主色调深色 */
    /* ... 其他颜色变量 */
}
```

### 添加图片

将图片放入 `static/images/` 目录：
- 产品图片: `product1.jpg`, `product2.jpg`, etc.
- 团队照片: `team1.jpg`, `team2.jpg`, etc.
- 二维码: `qrcode.png`

## 浏览器支持

- Chrome (最新版)
- Firefox (最新版)
- Safari (最新版)
- Edge (最新版)
- 移动端浏览器

## 部署平台

### Vercel（推荐）
- 免费套餐可用
- 自动部署
- 全球CDN
- Serverless Functions
- 支持 PostgreSQL

详细部署指南：查看 [VERCEL_DEPLOY.md](./VERCEL_DEPLOY.md)

### 其他平台
- Heroku
- Railway
- Render
- AWS Elastic Beanstalk
- Azure App Service

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 更新日志

### v1.0.0
- 初始版本
- 支持 Vercel 部署
- 完整的联系表单功能
- 响应式设计
- 管理后台

# Vercel 部署指南

## 前置要求

1. 注册 Vercel 账号: https://vercel.com
2. 安装 Vercel CLI (可选): `npm i -g vercel`
3. 准备 Git 仓库 (GitHub/GitLab/Bitbucket)

## 部署步骤

### 方法一：通过 Vercel 网站部署（推荐）

1. **登录 Vercel**
   - 访问 https://vercel.com
   - 使用 GitHub/GitLab/Bitbucket 账号登录

2. **导入项目**
   - 点击 "Add New Project"
   - 选择你的 Git 仓库
   - Vercel 会自动检测项目配置

3. **配置环境变量**
   在项目设置中添加以下环境变量：
   - `DATABASE_URL` - 数据库连接字符串（Vercel Postgres）
   - `SECRET_KEY` - Flask密钥（用于会话加密）

4. **配置数据库**
   - 在 Vercel 项目设置中，添加 "Postgres" 数据库
   - Vercel 会自动创建 `DATABASE_URL` 环境变量
   - 或者在环境变量中手动配置外部数据库连接

5. **部署**
   - 点击 "Deploy" 按钮
   - 等待部署完成
   - 访问提供的 URL

### 方法二：通过 Vercel CLI 部署

1. **安装 Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **登录 Vercel**
   ```bash
   vercel login
   ```

3. **部署项目**
   ```bash
   cd company_website
   vercel
   ```

4. **配置环境变量**
   ```bash
   vercel env add DATABASE_URL
   vercel env add SECRET_KEY
   ```

5. **生产环境部署**
   ```bash
   vercel --prod
   ```

## 数据库配置

### 选项1：使用 Vercel Postgres（推荐）

1. 在 Vercel 项目设置中添加 Postgres 数据库
2. Vercel 会自动提供 `POSTGRES_URL` 环境变量
3. 应用会自动使用该数据库

### 选项2：使用外部数据库

1. 使用 Supabase、PlanetScale、Railway 等数据库服务
2. 获取数据库连接字符串
3. 在 Vercel 环境变量中设置 `DATABASE_URL`

示例环境变量：
```
DATABASE_URL=postgresql://user:password@host:port/database
SECRET_KEY=your-secret-key-here
```

## 项目结构

```
company_website/
├── api/
│   └── index.py          # Vercel Serverless Function入口
├── templates/            # HTML模板
├── static/               # 静态文件（CSS、JS、图片）
├── requirements.txt      # Python依赖
├── vercel.json          # Vercel配置
└── .vercelignore        # Vercel忽略文件
```

## 环境变量说明

| 变量名 | 说明 | 必需 | 示例 |
|--------|------|------|------|
| `DATABASE_URL` | 数据库连接字符串 | 是 | `postgresql://user:pass@host/db` |
| `POSTGRES_URL` | Vercel Postgres连接字符串 | 否（如果使用Vercel Postgres） | 自动提供 |
| `SECRET_KEY` | Flask会话密钥 | 是 | `your-secret-key` |

## 静态文件

静态文件（CSS、JS、图片）会自动从 `static/` 目录提供。
确保静态文件路径在模板中正确引用。

## 常见问题

### 1. 数据库连接失败

**问题**: 应用无法连接到数据库

**解决方案**:
- 检查环境变量是否正确配置
- 确认数据库服务可访问
- 检查数据库连接字符串格式

### 2. 静态文件404

**问题**: CSS、JS文件无法加载

**解决方案**:
- 检查 `vercel.json` 中的路由配置
- 确认静态文件路径正确
- 清除浏览器缓存

### 3. 模板文件404

**问题**: 页面显示404错误

**解决方案**:
- 确认 `templates/` 目录存在
- 检查 `api/index.py` 中的模板路径配置
- 查看 Vercel 部署日志

### 4. 函数超时

**问题**: Serverless Function 执行超时

**解决方案**:
- 优化数据库查询
- 减少函数执行时间
- 考虑使用 Vercel Pro 计划（更长超时时间）

## 本地开发

### 使用 Vercel CLI 本地开发

```bash
vercel dev
```

这会启动本地开发服务器，模拟 Vercel 环境。

### 使用传统 Flask 开发服务器

```bash
python app.py
```

注意：本地开发需要使用 SQLite 或配置外部数据库。

## 自定义域名

1. 在 Vercel 项目设置中添加自定义域名
2. 按照提示配置 DNS 记录
3. 等待 DNS 传播完成

## 监控和日志

- 在 Vercel 控制台查看函数日志
- 使用 Vercel Analytics 监控性能
- 配置错误通知

## 更新部署

每次推送到 Git 仓库的主分支，Vercel 会自动重新部署。

也可以手动触发部署：
```bash
vercel --prod
```

## 技术支持

如遇问题，请查看：
- Vercel 文档: https://vercel.com/docs
- Vercel Python 运行时: https://vercel.com/docs/concepts/functions/serverless-functions/runtimes/python
- Flask 文档: https://flask.palletsprojects.com/


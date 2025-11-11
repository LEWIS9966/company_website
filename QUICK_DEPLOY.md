# 快速部署到 Vercel

## 5分钟快速部署

### 1. 准备Git仓库（如果还没有）

```bash
cd company_website
git init
git add .
git commit -m "Ready for Vercel deployment"
git remote add origin <your-github-repo-url>
git push -u origin main
```

### 2. 在Vercel上部署

1. 访问 https://vercel.com
2. 使用GitHub账号登录
3. 点击 "Add New Project"
4. 选择你的仓库
5. 点击 "Deploy"

### 3. 配置数据库（部署后）

#### 选项A: 使用Vercel Postgres（最简单）

1. 在Vercel项目设置中，点击 "Storage"
2. 创建 "Postgres" 数据库
3. Vercel会自动添加 `POSTGRES_URL` 环境变量
4. 重新部署项目

#### 选项B: 使用外部数据库

1. 创建Supabase/PlanetScale数据库
2. 获取连接字符串
3. 在Vercel项目设置中添加环境变量：
   - `DATABASE_URL` = `postgresql://user:pass@host/db`
   - `SECRET_KEY` = `your-secret-key`

### 4. 完成！

访问Vercel提供的URL，你的网站已经上线了！

## 环境变量配置

在Vercel项目设置 > Environment Variables 中添加：

| 变量名 | 值 | 说明 |
|--------|-----|------|
| `DATABASE_URL` | `postgresql://...` | 数据库连接（如果使用外部数据库） |
| `SECRET_KEY` | `your-secret-key` | Flask会话密钥 |

**注意**: 如果使用Vercel Postgres，`POSTGRES_URL` 会自动配置，无需手动添加。

## 测试部署

部署完成后，访问以下URL测试：

- 首页: `https://your-project.vercel.app/`
- 产品中心: `https://your-project.vercel.app/products`
- 公司简介: `https://your-project.vercel.app/about`
- 联系我们: `https://your-project.vercel.app/contact`
- 管理后台: `https://your-project.vercel.app/admin`

## 常见问题

### Q: 数据库连接失败？
A: 检查环境变量是否正确配置，确认数据库服务可访问。

### Q: 静态文件404？
A: 检查 `vercel.json` 配置，确认静态文件路径正确。

### Q: 页面显示500错误？
A: 查看Vercel函数日志，检查错误信息。

## 详细文档

- 完整部署指南: [VERCEL_DEPLOY.md](./VERCEL_DEPLOY.md)
- 部署检查清单: [DEPLOY_CHECKLIST.md](./DEPLOY_CHECKLIST.md)
- 项目README: [README.md](./README.md)


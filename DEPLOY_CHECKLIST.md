# Vercel 部署检查清单

## 部署前检查

### 1. 文件结构 ✅
- [x] `api/index.py` - Vercel Serverless Function入口
- [x] `templates/` - HTML模板目录
- [x] `static/` - 静态文件目录
- [x] `requirements.txt` - Python依赖
- [x] `vercel.json` - Vercel配置
- [x] `.vercelignore` - Vercel忽略文件

### 2. 配置文件 ✅
- [x] `vercel.json` - 路由配置正确
- [x] `requirements.txt` - 包含所有依赖
- [x] `api/index.py` - 导出app对象
- [x] 环境变量示例文件

### 3. 代码检查 ✅
- [x] Flask应用正确配置
- [x] 数据库连接使用环境变量
- [x] 静态文件路径正确
- [x] 模板路径正确
- [x] API路由正确

### 4. 环境变量配置
- [ ] `DATABASE_URL` - 数据库连接字符串
- [ ] `SECRET_KEY` - Flask会话密钥
- [ ] `POSTGRES_URL` - Vercel Postgres连接（如果使用）

## 部署步骤

### 步骤1: 准备Git仓库
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-repo-url>
git push -u origin main
```

### 步骤2: 在Vercel上创建项目
1. 登录 https://vercel.com
2. 点击 "Add New Project"
3. 选择你的Git仓库
4. 确认项目设置

### 步骤3: 配置环境变量
在Vercel项目设置中添加：
- `DATABASE_URL` - 数据库连接字符串
- `SECRET_KEY` - Flask会话密钥

### 步骤4: 配置数据库
**选项A: 使用Vercel Postgres（推荐）**
1. 在Vercel项目设置中，点击 "Storage"
2. 创建 Postgres 数据库
3. Vercel会自动提供 `POSTGRES_URL` 环境变量

**选项B: 使用外部数据库**
1. 创建Supabase/PlanetScale/Railway数据库
2. 获取数据库连接字符串
3. 在环境变量中设置 `DATABASE_URL`

### 步骤5: 部署
1. 点击 "Deploy" 按钮
2. 等待构建完成
3. 查看部署日志
4. 访问提供的URL

## 部署后检查

### 1. 功能测试
- [ ] 首页可以访问
- [ ] 产品中心可以访问
- [ ] 公司简介可以访问
- [ ] 联系我们页面可以访问
- [ ] 管理后台可以访问

### 2. 表单测试
- [ ] 联系表单可以提交
- [ ] 表单验证正常工作
- [ ] 数据保存到数据库
- [ ] 提交成功提示显示

### 3. 静态文件测试
- [ ] CSS样式正常加载
- [ ] JavaScript功能正常
- [ ] 图片正常显示

### 4. API测试
- [ ] `/api/submit-contact` 接口正常
- [ ] `/api/contacts` 接口正常
- [ ] 搜索功能正常
- [ ] 分页功能正常

## 常见问题解决

### 问题1: 数据库连接失败
**症状**: 提交表单时出现数据库错误

**解决方案**:
1. 检查环境变量是否正确配置
2. 确认数据库服务可访问
3. 检查数据库连接字符串格式
4. 查看Vercel函数日志

### 问题2: 静态文件404
**症状**: CSS、JS文件无法加载

**解决方案**:
1. 检查 `vercel.json` 中的路由配置
2. 确认静态文件路径正确
3. 检查 `api/index.py` 中的静态文件配置
4. 清除浏览器缓存

### 问题3: 模板文件404
**症状**: 页面显示404错误

**解决方案**:
1. 确认 `templates/` 目录存在
2. 检查 `api/index.py` 中的模板路径配置
3. 查看Vercel部署日志
4. 确认文件已推送到Git仓库

### 问题4: 函数超时
**症状**: Serverless Function 执行超时

**解决方案**:
1. 优化数据库查询
2. 减少函数执行时间
3. 考虑使用Vercel Pro计划（更长超时时间）
4. 检查数据库连接池配置

### 问题5: 环境变量未生效
**症状**: 应用无法读取环境变量

**解决方案**:
1. 确认环境变量已正确配置
2. 重新部署应用
3. 检查环境变量名称是否正确
4. 查看Vercel函数日志

## 性能优化

### 1. 数据库优化
- 使用连接池
- 优化查询语句
- 添加数据库索引
- 使用缓存

### 2. 静态文件优化
- 启用CDN缓存
- 压缩CSS和JS
- 优化图片大小
- 使用WebP格式

### 3. 函数优化
- 减少函数执行时间
- 优化数据库查询
- 使用缓存
- 减少依赖包大小

## 监控和维护

### 1. 日志监控
- 查看Vercel函数日志
- 监控错误率
- 检查响应时间

### 2. 数据库监控
- 监控数据库连接数
- 检查查询性能
- 监控存储使用量

### 3. 性能监控
- 使用Vercel Analytics
- 监控页面加载时间
- 检查API响应时间

## 更新部署

### 自动部署
每次推送到Git仓库的主分支，Vercel会自动重新部署。

### 手动部署
```bash
vercel --prod
```

### 回滚部署
在Vercel控制台中选择之前的部署版本进行回滚。

## 支持

如遇问题，请查看：
- Vercel文档: https://vercel.com/docs
- Vercel Python运行时: https://vercel.com/docs/concepts/functions/serverless-functions/runtimes/python
- Flask文档: https://flask.palletsprojects.com/
- 项目README: [README.md](./README.md)
- 部署指南: [VERCEL_DEPLOY.md](./VERCEL_DEPLOY.md)


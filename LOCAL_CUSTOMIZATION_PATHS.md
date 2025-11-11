# 本地可自定义路径与资源说明

面向本地开发与维护，列出除代码逻辑外可自定义的“路径/文件名/资源”及其含义，帮助你快速定位并统一线上与本地表现。

## 站点页面路径（路由）
- `/` — 首页（模板：`templates/index.html`）
- `/products` — 产品中心（模板：`templates/products.html`）
- `/about` — 公司简介（模板：`templates/about.html`）
- `/contact` — 联系我们（模板：`templates/contact.html`）
- `/admin` — 管理后台（模板：`templates/admin.html`）

说明：以上页面路径在本地由 `app.py` 提供，线上（Vercel）由 `api/index.py` 提供，模板与静态资源保持一致。

## API 路径（数据接口）
- `/api/submit-contact` — 联系表单提交接口（前端来源：`static/js/contact.js`）
- `/api/contacts` — 联系数据查询接口（管理后台使用）

说明：本地使用 SQLite（`contacts.db`），线上建议使用 Postgres；接口路径在本地与线上一致。

## 静态资源目录与命名约定
- 目录：`static/`
  - 样式：`static/css/style.css`
    - 主题变量（可改色）：定义在 `:root` 中
      - `--primary-color` — 主色（默认 `#2563eb`）
      - `--primary-dark` — 主色深色（默认 `#1e40af`）
      - `--secondary-color` — 次级色
      - `--text-color`/`--text-light` — 正文/辅助文字色
      - `--bg-color`/`--bg-light` — 背景色
      - `--border-color` — 边框色
      - `--success-color`/`--error-color` — 成功/错误提示色
      - `--shadow`/`--shadow-lg` — 阴影样式
  - 脚本：`static/js/`
    - `main.js` — 通用交互（页面导航等）
    - `contact.js` — 联系表单前端校验与提交（提交目标：`/api/submit-contact`；手机号/邮箱校验规则可调整）
  - 图片：`static/images/`
    - `qrcode.png` — 页脚二维码（引用自 `templates/base.html`）
    - `product1.jpg` ~ `product4.jpg` — 首页与产品页的产品示意图（引用自 `templates/index.html` / `templates/products.html`）
    - `team1.jpg` ~ `team3.jpg` — 公司简介页团队照片（引用自 `templates/about.html`）

说明：图片文件名需与模板引用一致；缺失时模板会展示占位图（`onerror`），视觉与本地可能不一致。

## 模板文件中常用可替换资源路径
- `templates/base.html`
  - 样式引入：`{{ url_for('static', filename='css/style.css') }}`
  - 脚本引入：`{{ url_for('static', filename='js/main.js') }}`
  - 二维码图片：`{{ url_for('static', filename='images/qrcode.png') }}`
  - 导航链接：`{{ url_for('index') }}` / `{{ url_for('products') }}` / `{{ url_for('about') }}` / `{{ url_for('contact') }}`
- `templates/index.html` / `templates/products.html`
  - 产品图片：`{{ url_for('static', filename='images/productX.jpg') }}`（X=1..4）
- `templates/about.html`
  - 团队图片：`{{ url_for('static', filename='images/teamX.jpg') }}`（X=1..3）
- `templates/contact.html`
  - 表单脚本：`{{ url_for('static', filename='js/contact.js') }}`

## 本地运行与脚本路径
- `run.bat` / `run.sh` / `启动网站*.bat` — 本地启动脚本（调用 `python app.py`）
- `start_server.py` — 备用启动脚本（加载 `app.py` 并运行）
- `test_server.py` — 本地测试脚本（提供 `/test` 路由）

## 本地数据库路径与含义
- `contacts.db` — 本地 SQLite 数据库文件（由 `app.py` 自动在项目根创建/使用）
  - 仅用于本地开发；不会被 Vercel 部署（被 `.vercelignore` 与 `.gitignore` 排除）。

## Vercel 相关（用于保持与本地一致）
- `vercel.json`
  - 构建入口：`api/index.py`（Python Serverless Function）
  - 静态直出：`/static/(.*)` → `/static/$1`
  - 其它路由：`/(.*)` → `api/index.py`
- `.vercelignore`
  - 排除：`app.py`、`*.db`、`test_server.py` 等（确保线上不使用本地 SQLite 与调试入口）
- 线上模板/静态目录映射
  - `api/index.py` 配置：`template_folder='../templates'`、`static_folder='../static'`、`static_url_path='/static'`

## 维护建议
- 新增/替换图片时：
  - 放入 `static/images/`，保持模板引用的文件名一致
  - 提交到仓库并重新部署，避免线上缺图导致占位图
- 调整主题色时：
  - 修改 `static/css/style.css` 中 `:root` 变量，可快速全站生效
- 修改联系信息时：
  - 更新 `templates/contact.html` 中的电话/邮箱/地址文案（如需隐藏某项可暂时注释对应块）
- 校验规则与接口：
  - 前端在 `static/js/contact.js` 可微调手机号/邮箱校验与提示文案；接口路径保持为 `/api/submit-contact`
- 数据一致性：
  - 本地使用 SQLite，线上使用 Postgres。若需数据统一，建议本地亦使用可连接的 Postgres，并在环境变量设置 `DATABASE_URL`

## 快速自检清单（视觉一致性）
- `static/images/` 是否包含模板引用的所有图片文件
- `static/css/style.css` 主题变量是否符合品牌视觉
- 页脚二维码 `qrcode.png` 是否存在并清晰
- 表单提交接口 `/api/submit-contact` 是否可达（本地/线上）
- 管理后台 `/admin` 是否能正常加载数据（本地 SQLite / 线上 Postgres）
"""
Vercel Serverless Function - 主入口点
Vercel Python运行时直接支持Flask WSGI应用
"""
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import logging
from sqlalchemy import desc

# 创建Flask应用
BASE_DIR = os.path.dirname(__file__)
TEMPLATES_DIR = os.path.join(BASE_DIR, '..', 'templates')
STATIC_DIR = os.path.join(BASE_DIR, '..', 'static')

app = Flask(
    __name__,
    template_folder=TEMPLATES_DIR,
    static_folder=STATIC_DIR,
    static_url_path='/static'
)

log_level = os.environ.get('LOG_LEVEL', 'INFO').upper()
logging.basicConfig(level=getattr(logging, log_level, logging.INFO), format='%(asctime)s %(levelname)s %(message)s')
app.logger.info("app_initialized templates=%s static=%s", TEMPLATES_DIR, STATIC_DIR)

# 数据库配置 - 使用环境变量
database_url = os.environ.get('DATABASE_URL') or os.environ.get('POSTGRES_URL')

if database_url and database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

DB_AVAILABLE = bool(database_url)

if DB_AVAILABLE:
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    enable_db = os.environ.get('ENABLE_DB', 'true').lower() == 'true'
    DB_AVAILABLE = enable_db
    if enable_db:
        # 临时 SQLite（Vercel 允许写 /tmp；数据不持久）
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/contacts.db'
    else:
        # 纯内存占位，后续 API 会返回 503 提示
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here-change-in-production')

_uri = app.config.get('SQLALCHEMY_DATABASE_URI')
_scheme = _uri.split(':', 1)[0] if _uri else 'none'
app.logger.info("db_config available=%s scheme=%s", DB_AVAILABLE, _scheme)

db = SQLAlchemy(app)

# 数据库模型
class Contact(db.Model):
    __tablename__ = 'contacts'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    requirements = db.Column(db.Text, nullable=False)
    submit_time = db.Column(db.DateTime, default=datetime.now)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'phone': self.phone,
            'email': self.email,
            'requirements': self.requirements,
            'submit_time': self.submit_time.strftime('%Y-%m-%d %H:%M:%S') if self.submit_time else ''
        }

# 初始化数据库
def init_db():
    if not DB_AVAILABLE:
        return
    try:
        with app.app_context():
            app.logger.info("init_db start")
            db.create_all()
            app.logger.info("init_db ok")
    except Exception as e:
        app.logger.exception("init_db error")
        # 在生产环境中，如果数据库未配置，这里会失败但不会阻止应用启动

 

# API路由
@app.route('/api/submit-contact', methods=['POST'])
def submit_contact():
    if not DB_AVAILABLE:
        app.logger.info("submit_contact unavailable_db")
        return jsonify({
            'success': False,
            'message': '当前未配置数据库，已收到提交但无法持久化，请稍后通过邮箱/WhatsApp联系'
        }), 503

    try:
        data = request.get_json()
        app.logger.info(
            "submit_contact received name=%s gender=%s phone=%s email=%s has_requirements=%s",
            bool(data and data.get('name')),
            bool(data and data.get('gender')),
            bool(data and data.get('phone')),
            bool(data and data.get('email')),
            bool(data and data.get('requirements'))
        )
        
        # 验证必填字段
        if not data or not data.get('name'):
            app.logger.info("submit_contact validation name_missing")
            return jsonify({'success': False, 'message': '请输入客户称呼'}), 400
        
        if not data.get('gender'):
            app.logger.info("submit_contact validation gender_missing")
            return jsonify({'success': False, 'message': '请选择性别'}), 400
        
        if not data.get('phone') and not data.get('email'):
            app.logger.info("submit_contact validation contact_missing")
            return jsonify({'success': False, 'message': '请至少填写手机或邮箱其中一项'}), 400
        
        if not data.get('requirements'):
            app.logger.info("submit_contact validation requirements_missing")
            return jsonify({'success': False, 'message': '请填写具体需求'}), 400
        
        # 验证手机号格式
        if data.get('phone') and len(data.get('phone')) < 10:
            app.logger.info("submit_contact validation phone_invalid")
            return jsonify({'success': False, 'message': '手机号格式不正确'}), 400
        
        # 验证邮箱格式
        if data.get('email') and '@' not in data.get('email'):
            app.logger.info("submit_contact validation email_invalid")
            return jsonify({'success': False, 'message': '邮箱格式不正确'}), 400
        
        # 初始化数据库
        init_db()
        
        # 创建新记录
        contact = Contact(
            name=data.get('name'),
            gender=data.get('gender'),
            phone=data.get('phone') or '',
            email=data.get('email') or '',
            requirements=data.get('requirements'),
            submit_time=datetime.now()
        )
        
        app.logger.info("submit_contact create")
        db.session.add(contact)
        db.session.commit()
        app.logger.info("submit_contact ok id=%s", contact.id)
        
        return jsonify({
            'success': True,
            'message': '提交成功！我们会尽快与您联系。'
        }), 200
        
    except Exception as e:
        if db.session:
            db.session.rollback()
        app.logger.exception("submit_contact error")
        return jsonify({'success': False, 'message': f'提交失败：{str(e)}'}), 500

@app.route('/api/contacts', methods=['GET'])
def get_contacts():
    """管理员查看联系表单数据"""
    if not DB_AVAILABLE:
        return jsonify({'success': False, 'message': '当前未配置数据库'}), 503
    try:
        app.logger.info("get_contacts start")
        init_db()
        # 支持查询参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        search = request.args.get('search', '')
        sort_by = request.args.get('sort_by', 'submit_time')
        app.logger.info("get_contacts params page=%s per_page=%s sort_by=%s search_len=%s", page, per_page, sort_by, len(search or ''))
        
        query = Contact.query
        
        # 搜索功能
        if search:
            query = query.filter(
                db.or_(
                    Contact.name.contains(search),
                    Contact.phone.contains(search),
                    Contact.email.contains(search),
                    Contact.requirements.contains(search)
                )
            )
        
        # 排序
        if sort_by == 'submit_time':
            query = query.order_by(desc(Contact.submit_time))
        elif sort_by == 'name':
            query = query.order_by(Contact.name)
        
        # 分页
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        contacts = pagination.items
        app.logger.info("get_contacts ok total=%s page=%s pages=%s count=%s", pagination.total, page, pagination.pages, len(contacts))
        
        return jsonify({
            'success': True,
            'data': [contact.to_dict() for contact in contacts],
            'total': pagination.total,
            'page': page,
            'per_page': per_page,
            'pages': pagination.pages
        }), 200
    
    except Exception as e:
        app.logger.exception("get_contacts error")
        return jsonify({'success': False, 'message': f'查询失败：{str(e)}'}), 500

# Vercel Python运行时需要导出app对象
# Vercel会自动识别Flask WSGI应用

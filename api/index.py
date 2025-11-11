"""
Vercel Serverless Function - 主入口点
Vercel Python运行时直接支持Flask WSGI应用
"""
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from sqlalchemy import desc

# 创建Flask应用
app = Flask(__name__, 
            template_folder='../templates',
            static_folder='../static',
            static_url_path='/static')

# 数据库配置 - 使用环境变量
database_url = os.environ.get('DATABASE_URL') or os.environ.get('POSTGRES_URL')
if database_url:
    # Vercel Postgres 或其他数据库（生产环境）
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    # 如果没有配置数据库，使用占位符（部署时需要配置Vercel Postgres）
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:pass@localhost/db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here-change-in-production')

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
    """初始化数据库表"""
    try:
        with app.app_context():
            db.create_all()
    except Exception as e:
        print(f"数据库初始化警告: {e}")
        # 在生产环境中，如果数据库未配置，这里会失败但不会阻止应用启动

# 页面路由
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/products')
def products():
    return render_template('products.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

# API路由
@app.route('/api/submit-contact', methods=['POST'])
def submit_contact():
    try:
        data = request.get_json()
        
        # 验证必填字段
        if not data or not data.get('name'):
            return jsonify({'success': False, 'message': '请输入客户称呼'}), 400
        
        if not data.get('gender'):
            return jsonify({'success': False, 'message': '请选择性别'}), 400
        
        if not data.get('phone') and not data.get('email'):
            return jsonify({'success': False, 'message': '请至少填写手机或邮箱其中一项'}), 400
        
        if not data.get('requirements'):
            return jsonify({'success': False, 'message': '请填写具体需求'}), 400
        
        # 验证手机号格式
        if data.get('phone') and len(data.get('phone')) < 10:
            return jsonify({'success': False, 'message': '手机号格式不正确'}), 400
        
        # 验证邮箱格式
        if data.get('email') and '@' not in data.get('email'):
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
        
        db.session.add(contact)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '提交成功！我们会尽快与您联系。'
        }), 200
        
    except Exception as e:
        if db.session:
            db.session.rollback()
        print(f"提交联系表单错误: {e}")
        return jsonify({'success': False, 'message': f'提交失败：{str(e)}'}), 500

@app.route('/api/contacts', methods=['GET'])
def get_contacts():
    """管理员查看联系表单数据"""
    try:
        # 初始化数据库
        init_db()
        
        # 支持查询参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        search = request.args.get('search', '')
        sort_by = request.args.get('sort_by', 'submit_time')
        
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
        
        return jsonify({
            'success': True,
            'data': [contact.to_dict() for contact in contacts],
            'total': pagination.total,
            'page': page,
            'per_page': per_page,
            'pages': pagination.pages
        }), 200
        
    except Exception as e:
        print(f"查询联系表单错误: {e}")
        return jsonify({'success': False, 'message': f'查询失败：{str(e)}'}), 500

# Vercel Python运行时需要导出app对象
# Vercel会自动识别Flask WSGI应用

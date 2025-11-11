from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from sqlalchemy import desc

app = Flask(__name__, 
            template_folder='templates',
            static_folder='static')

# 数据库配置
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'contacts.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'

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

# 创建数据库表
with app.app_context():
    db.create_all()

# 路由
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

@app.route('/api/submit-contact', methods=['POST'])
def submit_contact():
    try:
        data = request.get_json()
        
        # 验证必填字段
        if not data.get('name'):
            return jsonify({'success': False, 'message': '请输入客户称呼'}), 400
        
        if not data.get('gender'):
            return jsonify({'success': False, 'message': '请选择性别'}), 400
        
        if not data.get('phone') and not data.get('email'):
            return jsonify({'success': False, 'message': '请至少填写手机或邮箱其中一项'}), 400
        
        if not data.get('requirements'):
            return jsonify({'success': False, 'message': '请填写具体需求'}), 400
        
        # 验证手机号格式（简单验证）
        if data.get('phone') and len(data.get('phone')) < 10:
            return jsonify({'success': False, 'message': '手机号格式不正确'}), 400
        
        # 验证邮箱格式（简单验证）
        if data.get('email') and '@' not in data.get('email'):
            return jsonify({'success': False, 'message': '邮箱格式不正确'}), 400
        
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
        db.session.rollback()
        return jsonify({'success': False, 'message': f'提交失败：{str(e)}'}), 500

@app.route('/api/contacts', methods=['GET'])
def get_contacts():
    """管理员查看联系表单数据"""
    try:
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
        return jsonify({'success': False, 'message': f'查询失败：{str(e)}'}), 500

if __name__ == '__main__':
    print("=" * 60)
    print("企业展示网站服务器启动中...")
    print("=" * 60)
    print("\n访问地址: http://127.0.0.1:5000")
    print("        或 http://localhost:5000")
    print("\n主要页面:")
    print("  - 首页: http://127.0.0.1:5000")
    print("  - 产品中心: http://127.0.0.1:5000/products")
    print("  - 公司简介: http://127.0.0.1:5000/about")
    print("  - 联系我们: http://127.0.0.1:5000/contact")
    print("  - 管理后台: http://127.0.0.1:5000/admin")
    print("\n按 Ctrl+C 停止服务器")
    print("=" * 60)
    print()
    try:
        app.run(debug=True, host='127.0.0.1', port=5000, use_reloader=False)
    except OSError as e:
        if 'Address already in use' in str(e) or '地址已在使用' in str(e):
            print(f"\n错误: 端口5000已被占用，请关闭其他使用该端口的程序")
            print("或者修改app.py中的端口号（例如改为5001）")
        else:
            print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()
        input("\n按回车键退出...")


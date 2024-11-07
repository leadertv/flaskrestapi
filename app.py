from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)

# Конфиг базы данных и JWT
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ads.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = '123867' # Тут любое и что угодно
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Модель юзера
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Модель объявления
class Ad(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    owner = db.relationship('User', backref=db.backref('ads', lazy=True))

# Инициализация бд
with app.app_context():
    db.create_all()

# Рег юзера
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or 'email' not in data or 'password' not in data:
        abort(400, 'Необходимо указать email и пароль')

    if User.query.filter_by(email=data['email']).first():
        abort(400, 'Пользователь с таким email уже существует')

    user = User(email=data['email'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'Пользователь зарегистрирован'}), 201

# Вход юзера
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'email' not in data or 'password' not in data:
        abort(400, 'Необходимо указать email и пароль')

    user = User.query.filter_by(email=data['email']).first()
    if user is None or not user.check_password(data['password']):
        abort(401, 'Неверные учетные данные')

    access_token = create_access_token(identity=user.id)
    return jsonify({'access_token': access_token}), 200

# Создание объявления (POST) - только для авторизованных пользователей
@app.route('/ads', methods=['POST'])
@jwt_required()
def create_ad():
    data = request.get_json()
    user_id = get_jwt_identity()
    if not data or 'title' not in data or 'description' not in data:
        abort(400, 'Недостаточно данных для создания объявления')

    ad = Ad(
        title=data['title'],
        description=data['description'],
        owner_id=user_id
    )
    db.session.add(ad)
    db.session.commit()

    return jsonify({'message': 'Объявление создано', 'ad': {
        'id': ad.id,
        'title': ad.title,
        'description': ad.description,
        'created_at': ad.created_at,
        'owner_id': ad.owner_id
    }}), 201

# Получение объявления по ID (GET)
@app.route('/ads/<int:ad_id>', methods=['GET'])
def get_ad(ad_id):
    ad = Ad.query.get_or_404(ad_id)
    return jsonify({
        'id': ad.id,
        'title': ad.title,
        'description': ad.description,
        'created_at': ad.created_at,
        'owner_id': ad.owner_id
    }), 200

# Удаление объявления по ID (DELETE) - только для владельца
@app.route('/ads/<int:ad_id>', methods=['DELETE'])
@jwt_required()
def delete_ad(ad_id):
    user_id = get_jwt_identity()
    ad = Ad.query.get_or_404(ad_id)
    if ad.owner_id != user_id:
        abort(403, 'Вы не являетесь владельцем данного объявления')

    db.session.delete(ad)
    db.session.commit()
    return jsonify({'message': 'Объявление удалено'}), 200

# Запуск приложения
if __name__ == '__main__':
    app.run(debug=True)


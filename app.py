from flask import Flask, request, jsonify
from models import db, User
from config import Config
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config.from_object(Config)
db.init_app(app)

def create_initial_users():
    # Verificar si ya existen usuarios para no duplicar
    if not User.query.filter_by(email='admin@example.com').first():
        admin_user = User(
            username='admin',
            email='admin@example.com',
            password='admin123',
            role='admin'
        )
        db.session.add(admin_user)
    
    if not User.query.filter_by(email='adminP@example.com').first():
        adminp_user = User(
            username='adminP',
            email='adminP@example.com',
            password='adminP123',
            role='adminP'
        )
        db.session.add(adminp_user)
    
    db.session.commit()

with app.app_context():
    db.create_all()
    create_initial_users()

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not all(key in data for key in ['username', 'email', 'password', 'role']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400

    new_user = User(
        username=data['username'],
        email=data['email'],
        password=data['password'],
        role=data['role']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({
        'message': 'User created successfully',
        'user': {
            'id': new_user.id,
            'username': new_user.username,
            'email': new_user.email,
            'role': new_user.role
        }
    }), 201

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([
        {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'password': user.password,
            'role': user.role
        } for user in users
    ])

@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'password': user.password,
        'role': user.role
    })

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    user = User.query.get_or_404(id)
    
    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        user.email = data['email']
    if 'password' in data:
        user.password = data['password']
    if 'role' in data:
        user.role = data['role']
    
    db.session.commit()
    return jsonify({
        'message': 'User updated successfully',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role
        }
    })

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
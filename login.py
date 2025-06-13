# login.py
from flask import Blueprint, request, jsonify
from models import db, User

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user and user.password == password:
        return jsonify({'message': 'Login exitoso'}), 200
    else:
        return jsonify({'message': 'Credenciales inválidas'}), 401

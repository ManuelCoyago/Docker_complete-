from flask import Flask, request, jsonify
from models import db, User
from config import Config
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()
    
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Email y contraseña son requeridos'}), 400

    user = User.query.filter_by(email=email).first()
    
    if user and user.password == password:
        role = user.role if user.role else 'user'

        # Llamar al servicio de productos (solo si no es admin)
        products = []
        if role != 'admin':
            try:
                response = requests.get("http://webp:5000/products")
                if response.ok:
                    products = response.json()
            except Exception as e:
                print(f"Error obteniendo productos: {str(e)}")

        # Todos los usuarios requieren 2FA
        return jsonify({
            'requires_2fa': True,
            'email': user.email,
            'role': role,
            'products': products if products else []
        }), 200

    else:
        return jsonify({'message': 'Credenciales inválidas'}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
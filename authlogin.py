from flask import Flask, request, jsonify
import pyotp, qrcode, base64
from io import BytesIO
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)  # ya lo tienes bien así


@app.route('/generate-2fa', methods=['POST', 'OPTIONS'])
def generate_2fa():
    if request.method == 'OPTIONS':
        return '', 200  # Solo responde OK para el preflight CORS
    
    email = request.json.get('email')
    secret = pyotp.random_base32()
    
    uri = pyotp.totp.TOTP(secret).provisioning_uri(name=email, issuer_name="TuApp")
    img = qrcode.make(uri)
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    qr_base64 = base64.b64encode(buffered.getvalue()).decode()
    
    return jsonify({
        'secret': secret,
        'qr_code': f"data:image/png;base64,{qr_base64}"
    })


@app.route('/verify-2fa', methods=['POST'])
def verify_2fa():
    secret = request.json.get('secret')
    token = request.json.get('token')

    if not secret or not token:
        return jsonify({'valid': False, 'error': 'Secreto o token faltante'}), 400
    
    try:
        if pyotp.TOTP(secret).verify(token):
            return jsonify({'valid': True})
        return jsonify({'valid': False}), 401
    except Exception as e:
        print(f"Error verificando 2FA: {str(e)}")
        return jsonify({'valid': False, 'error': 'Error interno al verificar 2FA'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
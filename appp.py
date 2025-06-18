from flask import Flask, jsonify,request
from flask_cors import CORS
from models import dbp, Product
from config import ConfigP

app = Flask(__name__)
CORS(app)
app.config.from_object(ConfigP)
dbp.init_app(app)

def create_initial_products():
    # Verificar si ya existen productos para no duplicar
    if not Product.query.first():
        product1 = Product(
            name='Laptop Premium',
            description='Laptop de última generación con 16GB RAM',
            price=1299.99
        )
        product2 = Product(
            name='Smartphone Pro',
            description='Teléfono inteligente con cámara 108MP',
            price=899.99
        )
        dbp.session.add_all([product1, product2])
        dbp.session.commit()

with app.app_context():
    dbp.create_all()
    create_initial_products()  # Crear productos iniciales al iniciar



@app.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    new_product = Product(name=data['name'], description=data.get('description'), price=data['price'])
    dbp.session.add(new_product)
    dbp.session.commit()
    return jsonify({'message': 'Product created successfully'}), 201

@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{'id': product.id, 'name': product.name, 'description': product.description, 'price': product.price} for product in products])



@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get_or_404(id)
    return jsonify({'id': product.id, 'name': product.name, 'description': product.description, 'price': product.price})


@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    data = request.get_json()
    product = Product.query.get_or_404(id)
    product.name = data['name']
    product.description = data.get('description', product.description)
    product.price = data['price']
    dbp.session.commit()
    return jsonify({'message': 'Product updated successfully'})

@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    dbp.session.delete(product)
    dbp.session.commit()
    return jsonify({'message': 'Product deleted successfully'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

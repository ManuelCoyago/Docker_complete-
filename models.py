from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
dbp = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)  # Nuevo campo

    def __repr__(self):
        return f'<User {self.username}>'

class Product(dbp.Model):
    id = dbp.Column(db.Integer, primary_key=True)
    name = dbp.Column(db.String(80), nullable=False)
    description = dbp.Column(db.String(200), nullable=True)
    price = dbp.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Product {self.name}>'

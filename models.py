from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4

db = SQLAlchemy()

def get_uuid():
    return uuid4().hex

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    email = db.Column(db.String(345), unique=True)
    password = db.Column(db.Text, nullable=False)

class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    name = db.Column(db.String(345))
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.Text, nullable=False)

class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    
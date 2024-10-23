import json
from flask import Flask, request, jsonify, session
from models import User, Product, Order, db
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity, \
                               unset_jwt_cookies, jwt_required, JWTManager

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "snapnet_interview_test"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
jwt = JWTManager(app)

db.init_app(app)

# The following route are the authentication route for the application
@app.route('/login', methods=["POST"])
def create_token():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    if User.query.filter_by(email=email).first():
        access_token = create_access_token(identity=email)
        response = {"access_token": access_token, "message": "Login SuccessFully"}
        return response, 200

    return {"msg": "Wrong email or password"}, 401

@app.route('/signup', methods=["POST"])
def register():

    db.create_all()
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already exists'}), 400

    new_user = User(email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    access_token = create_access_token(identity=email)
    return jsonify({'message': 'User registered successfully!'}), 201

@app.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response, 200



####################################################################
# The following endpoints are for managing and filtering of products.

# This is the endpoint to add some product to the product table
@app.route("/add_product", methods=["POST"])
@jwt_required()
def add_product():

    data = request.get_json()
    name = data.get('name')
    price = data.get('price')
    description = data.get('description')
    quantity = data.get('quantity')
    image_url = data.get('image_url')

    new_product = Product(name=name, price=price, description=description, quantity=quantity, image_url=image_url)
    db.session.add(new_product)
    db.session.commit()

    return jsonify({'message': 'Product Created Successfully'}), 201

#This endpoint is used for editing product
@app.route("/edit_product", methods=["PUT"])
@jwt_required()
def edit_product():
    data = request.get_json()
    product_name = data.get('name')
    name = data.get('name')
    price = data.get('price')
    description = data.get('description')
    quantity = data.get('quantity')
    image_url = data.get('image_url')

    product = Product.query.filter_by(name=name).first()

    product.name = name
    product.price = price
    product.description = description
    product.quantity = quantity
    product.image_url = image_url

    db.session.add(product)
    db.session.commit()

    return jsonify({'message': 'Product Updated Successfully'}), 200

# This endpoint is used to get a product
@app.route("/get_product", methods=["GET"])
def get_product():
    data = request.get_json()
    name = data.get('name')
    product = Product.query.filter_by(name=name).first()

    return jsonify({"name":product.name, "price": product.price, "description": product.description, "quantity": product.quantity, "image_url": product.image_url}), 200
#####################


# The following endpoints are for managing and filtering of orders.
@app.route("/add_order", methods=["POST"])
@jwt_required()
def add_Order():

    data = request.get_json()
    user_id = data.get('user_id')
    product_id = data.get('product_id')
    shipping_address = data.get('shipping_address')

    new_order = Product(user_id=user_id, product_id=product_id, shipping_address=shipping_address)
    db.session.add(new_order)
    db.session.commit()

    return jsonify({'message': 'Order Created Successfully'}), 200

# This endpoint is used to get an order
@app.route("/get_order", methods=["GET"])
@jwt_required()
def get_order():
    data = request.get_json()
    order_id = data.get('order_id')
    order = Order.query.filter_by(id=order_id).first()

    return jsonify({"user_id": order.user_id, "product_id": order.product_id, "shipping_address": order.shipping_address}), 200


if __name__ == "__main__":
    app.run(debug=True)


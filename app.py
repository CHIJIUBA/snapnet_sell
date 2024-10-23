import json
from flask import Flask, request, jsonify, session
from models import User, db
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity, \
                               unset_jwt_cookies, jwt_required, JWTManager

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "snapnet_interview_test"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
jwt = JWTManager(app)

db.init_app(app)

@app.route('/login', methods=["POST"])
def create_token():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    if email != "test" or password != "test":
        return {"msg": "Wrong email or password"}, 401

    access_token = create_access_token(identity=email)
    response = {"access_token": access_token}
    return response, 200

@app.route('/signup', methods=["POST"])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already exists'}), 400

    return jsonify({'message': 'User registered successfully!'}), 201

    # new_user = User(email=email, password=password)
    # db.session.add(new_user)
    # db.session.commit()

    # # access_token = create_access_token(identity=email)
    # return jsonify({'message': 'User registered successfully!'}), 201


@app.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response, 200


if __name__ == "__main__":
    app.run(debug=True)


from flask import Flask, request, jsonify
from config import Config
from models import db, User
from flask_cors import CORS

from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

db.init_app(app)
jwt = JWTManager(app)

with app.app_context():
    db.create_all()
    print("Database Created Successfully")


@app.route("/")
def home():
    return "Welcome to Trekking Management Application"


# -------------------- Register --------------------

@app.route("/register", methods=["POST"])
def register():

    data = request.get_json()
    if not data:
        return jsonify({
        "message": "Invalid request"
    }), 400

    existing_user = User.query.filter_by(email=data["email"]).first()

    if existing_user:
        return jsonify({
        "message": "Email already registered"
    }), 400

    hashed_password = generate_password_hash(data["password"])

    user = User(
        name=data["name"],
        email=data["email"],
        password=hashed_password,
        role="user"
    )

    try:
        db.session.add(user)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({
            "message": "Registration Failed"
        }), 500
    return jsonify({
        "message": "User Registered Successfully"
    }), 201


# -------------------- Login --------------------

@app.route("/login", methods=["POST"])
def login():

    data = request.get_json()
    if not data:
        return jsonify({
        "message": "Invalid request"
    }), 400

    if "email" not in data or "password" not in data:
        return jsonify({
        "message": "Email and Password are required"
    }), 400

    user = User.query.filter_by(email=data["email"]).first()

    if not user:
        return jsonify({
            "message": "User not found"
        }), 404
    
    if not check_password_hash(user.password, data["password"]):
        return jsonify({
            "message": "Invalid Password"
        }), 401

    token = create_access_token(identity=str(user.id))

    return jsonify({
        "message": "Login Successful",
        "access_token": token
    }), 200


# -------------------- Protected Route --------------------

@app.route("/profile", methods=["GET"])
@jwt_required()
def profile():

    current_user = get_jwt_identity()

    return jsonify({
        "message": "Protected Route",
        "user_id": current_user
    }), 200


if __name__ == "__main__":
    app.run(debug=True)
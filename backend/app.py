from flask import Flask, request, jsonify
from config import Config
from models import db, User, Trek
from werkzeug.security import generate_password_hash
from flask_cors import CORS
from datetime import datetime

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

    admin = User.query.filter_by(email="admin@gmail.com").first()

    if not admin:

        admin = User(
            name="Admin",
            email="admin@gmail.com",
            password=generate_password_hash("admin123"),
            role="admin"
        )

        db.session.add(admin)
        db.session.commit()

        print("Default Admin Created")

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

    user = User.query.get(int(current_user))

    if not user:
        return jsonify({
            "message": "User not found"
        }), 404

    return jsonify({
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role
    }), 200


# -------------------- Get Treks --------------------

@app.route("/treks", methods=["GET"])
@jwt_required()
def get_treks():

    treks = Trek.query.all()

    trek_list = []

    for trek in treks:
        trek_list.append({
            "id": trek.id,
            "name": trek.name,
            "location": trek.location,
            "difficulty": trek.difficulty,
            "duration": trek.duration
        })

    return jsonify(trek_list), 200
# -------------------- Create Trek --------------------

@app.route("/treks", methods=["POST"])
@jwt_required()
def create_trek():

    current_user = get_jwt_identity()

    user = User.query.get(int(current_user))

    if user.role != "admin":
        return jsonify({
            "message": "Only Admin Can Create Trek"
        }), 403

    data = request.get_json()

    trek = Trek(
    name=data["name"],
    location=data["location"],
    difficulty=data["difficulty"],
    duration=data["duration"],
    available_slots=data["available_slots"],
    status=data["status"],
    start_date=datetime.strptime(
        data["start_date"],
        "%Y-%m-%d"
    ).date(),
    end_date=datetime.strptime(
        data["end_date"],
        "%Y-%m-%d"
    ).date()
)

    db.session.add(trek)
    db.session.commit()

    return jsonify({
        "message": "Trek Created Successfully"
    }), 201
# -------------------- Delete Trek --------------------

@app.route("/treks/<int:trek_id>", methods=["DELETE"])
@jwt_required()
def delete_trek(trek_id):

    current_user = get_jwt_identity()

    user = User.query.get(int(current_user))

    if user.role != "admin":
        return jsonify({
            "message": "Only Admin Can Delete Trek"
        }), 403

    trek = Trek.query.get(trek_id)

    if not trek:
        return jsonify({
            "message": "Trek Not Found"
        }), 404

    db.session.delete(trek)
    db.session.commit()

    return jsonify({
        "message": "Trek Deleted Successfully"
    }), 200

if __name__ == "__main__":
    app.run(debug=True)
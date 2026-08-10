from flask import Flask, request, jsonify
from config import Config
from models import db, User, Trek, Booking
from werkzeug.security import generate_password_hash
from flask_cors import CORS
from datetime import datetime
from flask_caching import Cache
import os
import csv


from flask import send_file

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
app.config["CACHE_TYPE"] = "RedisCache"
app.config["CACHE_REDIS_URL"] = "redis://localhost:6379/0"
app.config["CACHE_DEFAULT_TIMEOUT"] = 60


db.init_app(app)
jwt = JWTManager(app)
cache = Cache(app)

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
    if (
        not data.get("name") or
        not data.get("email") or
        not data.get("password")
    ):
        return jsonify({
            "message": "All Fields Are Required"
        }), 400

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
    
    if not user.active:
        return jsonify({
            "message": "Your Account Has Been Deactivated"
        }), 403
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
@cache.cached(timeout=60)
def get_treks():

    current_user = get_jwt_identity()

    user = User.query.get(int(current_user))

    if user.role == "admin":

        treks = Trek.query.all()

    else:

        treks = Trek.query.filter_by(
            status="Open"
        ).all()

    trek_list = []

    for trek in treks:

        trek_list.append({

            "id": trek.id,
            "name": trek.name,
            "location": trek.location,
            "difficulty": trek.difficulty,
            "duration": trek.duration,
            "available_slots": trek.available_slots,
            "status": trek.status,
            "start_date": trek.start_date.strftime("%Y-%m-%d"),
            "end_date": trek.end_date.strftime("%Y-%m-%d"),
            "assigned_staff_id": trek.assigned_staff_id,
            "assigned_staff": (
                trek.staff.name
                if trek.staff
                else "Not Assigned"
            )

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

    if (
        not data.get("name") or
        not data.get("name").strip() or
        not data.get("location") or
        not data.get("location").strip() or
        not data.get("difficulty") or
        not data.get("difficulty").strip() or
        not data.get("duration") or
        not data.get("available_slots") or
        not data.get("start_date") or
        not data.get("end_date")
    ):
        return jsonify({
            "message": "All Fields Are Required"
        }), 400

    if int(data["available_slots"]) < 1:
        return jsonify({
            "message": "Available Slots Must Be Greater Than 0"
        }), 400

    start_date = datetime.strptime(
        data["start_date"], "%Y-%m-%d"
    ).date()

    end_date = datetime.strptime(
        data["end_date"], "%Y-%m-%d"
    ).date()

    if end_date < start_date:
        return jsonify({
            "message": "End Date Must Be Greater Than or Equal To Start Date"
        }), 400

    actual_duration = (end_date - start_date).days + 1

    if actual_duration != int(data["duration"]):
        return jsonify({
            "message": "Duration Must Match Start Date And End Date"
        }), 400

    trek = Trek(
        name=data["name"].strip(),
        location=data["location"].strip(),
        difficulty=data["difficulty"].strip(),
        duration=data["duration"],
        available_slots=data["available_slots"],
        status="Upcoming",
        assigned_staff_id=data.get("assigned_staff_id"),
        start_date=start_date,
        end_date=end_date
    )

    db.session.add(trek)
    db.session.commit()

    cache.clear()

    return jsonify({
        "message": "Trek Created Successfully",
        "id": trek.id
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

    existing_booking = Booking.query.filter_by(
        trek_id=trek_id
    ).first()

    if existing_booking:
        return jsonify({
            "message": "Cannot Delete Trek Because Bookings Exist"
        }), 400

    db.session.delete(trek)
    db.session.commit()

    cache.clear()

    return jsonify({
        "message": "Trek Deleted Successfully"
    }), 200
# -------------------- Update Trek --------------------
@app.route("/treks/<int:trek_id>", methods=["PUT"])
@jwt_required()
def update_trek(trek_id):

    current_user = get_jwt_identity()

    user = User.query.get(int(current_user))

    if user.role != "admin":
        return jsonify({
            "message": "Only Admin Can Update Trek"
        }), 403

    trek = Trek.query.get(trek_id)

    if not trek:
        return jsonify({
            "message": "Trek Not Found"
        }), 404

    data = request.get_json()

    if (
        not data.get("name") or
        not data.get("name").strip() or
        not data.get("location") or
        not data.get("location").strip() or
        not data.get("difficulty") or
        not data.get("difficulty").strip() or
        not data.get("duration") or
        not data.get("available_slots") or
        not data.get("status") or
        not data.get("start_date") or
        not data.get("end_date")
    ):
        return jsonify({
            "message": "All Fields Are Required"
        }), 400

    if int(data["available_slots"]) < 1:
        return jsonify({
            "message": "Available Slots Must Be Greater Than 0"
        }), 400

    start_date = datetime.strptime(
        data["start_date"], "%Y-%m-%d"
    ).date()

    end_date = datetime.strptime(
        data["end_date"], "%Y-%m-%d"
    ).date()

    if end_date < start_date:
        return jsonify({
            "message": "End Date Must Be Greater Than or Equal To Start Date"
        }), 400

    actual_duration = (end_date - start_date).days + 1

    if actual_duration != int(data["duration"]):
        return jsonify({
            "message": "Duration Must Match Start Date And End Date"
        }), 400

    trek.name = data["name"].strip()
    trek.location = data["location"].strip()
    trek.difficulty = data["difficulty"].strip()
    trek.duration = data["duration"]
    trek.available_slots = data["available_slots"]
    trek.status = data["status"]
    trek.assigned_staff_id = data.get("assigned_staff_id")
    trek.start_date = start_date
    trek.end_date = end_date

    db.session.commit()
    cache.clear()

    return jsonify({
        "message": "Trek Updated Successfully"
    }), 200
# -------------------- Book Trek --------------------

@app.route("/book/<int:trek_id>", methods=["POST"])
@jwt_required()
def book_trek(trek_id):

    current_user = get_jwt_identity()

    trek = Trek.query.get(trek_id)

    if not trek:
        return jsonify({
            "message": "Trek Not Found"
        }), 404
    if trek.status != "Open":
        return jsonify({
            "message": "Booking Allowed Only For Open Treks"
        }), 400

    if trek.available_slots <= 0:
        return jsonify({
            "message": "No Slots Available"
        }), 400

    existing_booking = Booking.query.filter_by(
        user_id=int(current_user),
        trek_id=trek_id
    ).first()

    if existing_booking:
        return jsonify({
            "message": "You Have Already Booked This Trek"
        }), 400

    booking = Booking(
        user_id=int(current_user),
        trek_id=trek.id,
        status="Pending"
    )

    db.session.add(booking)
    trek.available_slots -= 1
    db.session.commit()

    return jsonify({
        "message": "Trek Booked Successfully"
    }), 201
@app.route("/mybookings", methods=["GET"])
@jwt_required()
def my_bookings():

    current_user = get_jwt_identity()

    bookings = Booking.query.filter_by(
        user_id=int(current_user)
    ).all()

    result = []

    for booking in bookings:

        trek = Trek.query.get(booking.trek_id)

        if not trek:
            continue

        result.append({
            "booking_id": booking.id,
            "trek_name": trek.name,
            "booking_date": booking.booking_date,
            "status": booking.status
        })

    return jsonify(result), 200
@app.route("/allbookings", methods=["GET"])
@jwt_required()
def all_bookings():

    current_user = get_jwt_identity()

    user = User.query.get(int(current_user))

    if user.role != "admin":
        return jsonify({
            "message": "Only Admin Can View All Bookings"
        }), 403

    bookings = Booking.query.all()

    result = []

    for booking in bookings:

        trek = Trek.query.get(booking.trek_id)
        booked_user = User.query.get(booking.user_id)

        if not trek or not booked_user:
            continue

        result.append({
            "booking_id": booking.id,
            "user_name": booked_user.name,
            "trek_name": trek.name,
            "booking_date": booking.booking_date,
            "status": booking.status
        })

    return jsonify(result), 200
@app.route("/approve/<int:booking_id>", methods=["PUT"])
@jwt_required()
def approve_booking(booking_id):

    current_user = get_jwt_identity()

    user = User.query.get(int(current_user))

    if user.role != "admin":
        return jsonify({
            "message": "Only Admin Can Approve Booking"
        }), 403

    booking = Booking.query.get(booking_id)
    if booking.status == "Approved":
        return jsonify({
            "message": "Booking Already Approved"
    }), 400
    if not booking:
        return jsonify({
            "message": "Booking Not Found"
        }), 404

    booking.status = "Approved"

    db.session.commit()

    return jsonify({
        "message": "Booking Approved Successfully"
    }), 200
# -------------------- Add Staff --------------------

@app.route("/staff", methods=["POST"])
@jwt_required()
def add_staff():

    current_user = get_jwt_identity()

    user = User.query.get(int(current_user))

    if user.role != "admin":
        return jsonify({
            "message": "Only Admin Can Add Staff"
        }), 403

    data = request.get_json()
    if (
        not data.get("name") or
        not data.get("email") or
        not data.get("password")
    ):
        return jsonify({
            "message": "All Fields Are Required"
        }), 400

    existing_staff = User.query.filter_by(
        email=data["email"]
    ).first()

    if existing_staff:
        return jsonify({
            "message": "Email Already Exists"
        }), 400

    staff = User(
        name=data["name"],
        email=data["email"],
        password=generate_password_hash(data["password"]),
        role="staff"
    )

    db.session.add(staff)
    db.session.commit()

    return jsonify({
        "message": "Staff Added Successfully"
    }), 201
# -------------------- Get Staff --------------------

@app.route("/staff", methods=["GET"])
@jwt_required()
def get_staff():

    current_user = get_jwt_identity()

    user = User.query.get(int(current_user))

    if user.role != "admin":
        return jsonify({
            "message": "Only Admin Can View Staff"
        }), 403

    staffs = User.query.filter_by(
        role="staff",
        active=True
    ).all()
    result = []

    for staff in staffs:

        result.append({
    "id": staff.id,
    "name": staff.name,
    "email": staff.email,
    "active": staff.active
    })

    return jsonify(result), 200
# -------------------- Assign Staff --------------------

@app.route("/assign/<int:trek_id>", methods=["PUT"])
@jwt_required()
def assign_staff(trek_id):

    current_user = get_jwt_identity()

    user = User.query.get(int(current_user))

    if user.role != "admin":
        return jsonify({
            "message": "Only Admin Can Assign Staff"
        }), 403

    trek = Trek.query.get(trek_id)

    if not trek:
        return jsonify({
            "message": "Trek Not Found"
        }), 404

    data = request.get_json()

    staff = User.query.get(data["staff_id"])

    if not staff or staff.role != "staff":
        return jsonify({
            "message": "Invalid Staff"
        }), 400

    trek.assigned_staff_id = staff.id

    db.session.commit()

    return jsonify({
        "message": "Staff Assigned Successfully"
    }), 200
# -------------------- Staff Treks --------------------

@app.route("/staff/treks", methods=["GET"])
@jwt_required()
def staff_treks():

    current_user = get_jwt_identity()

    user = User.query.get(int(current_user))

    if user.role != "staff":
        return jsonify({
            "message": "Only Staff Can View Assigned Treks"
        }), 403

    treks = Trek.query.filter_by(
        assigned_staff_id=user.id
    ).all()

    result = []

    for trek in treks:
        participant_count = Booking.query.filter_by(
            trek_id=trek.id
        ).count()
        result.append({
            "id": trek.id,
            "name": trek.name,
            "location": trek.location,
            "difficulty": trek.difficulty,
            "duration": trek.duration,
            "available_slots": trek.available_slots,
            "status": trek.status,
            "participant_count": participant_count
        })

    return jsonify(result), 200
# -------------------- Staff Update Trek --------------------

@app.route("/staff/treks/<int:trek_id>", methods=["PUT"])
@jwt_required()
def update_staff_trek(trek_id):

    current_user = get_jwt_identity()

    user = User.query.get(int(current_user))
    current_user = get_jwt_identity()

    user = User.query.get(int(current_user))

    print("Current User ID:", current_user)
    print("Role:", user.role)
    if user.role != "staff":
        return jsonify({
            "message": "Only Staff Can Update Trek"
        }), 403

    trek = Trek.query.get(trek_id)

    if not trek:
        return jsonify({
            "message": "Trek Not Found"
        }), 404

    if trek.assigned_staff_id != user.id:
        return jsonify({
            "message": "This Trek Is Not Assigned To You"
        }), 403

    data = request.get_json()

    trek.available_slots = data["available_slots"]
    trek.status = data["status"]

    db.session.commit()

    return jsonify({
        "message": "Trek Updated Successfully"
    }), 200
@app.route("/staff/treks/<int:trek_id>/participants", methods=["GET"])
@jwt_required()
def trek_participants(trek_id):

    current_user = get_jwt_identity()

    user = User.query.get(int(current_user))

    if user.role != "staff":
        return jsonify({
            "message": "Only Staff Can View Participants"
        }), 403

    trek = Trek.query.get(trek_id)

    if not trek:
        return jsonify({
            "message": "Trek Not Found"
        }), 404

    if trek.assigned_staff_id != user.id:
        return jsonify({
            "message": "This Trek Is Not Assigned To You"
        }), 403

    bookings = Booking.query.filter_by(
        trek_id=trek_id
    ).all()

    result = []

    for booking in bookings:

        participant = User.query.get(booking.user_id)

        result.append({
            
            "id": participant.id,
            "name": participant.name,
            "email": participant.email,
            "status": booking.status
        })

    return jsonify(result), 200


# -------------------- Activate / Deactivate Staff --------------------

@app.route("/staff/<int:staff_id>", methods=["PUT"])
@jwt_required()
def update_staff_status(staff_id):

    current_user = get_jwt_identity()

    admin = User.query.get(int(current_user))

    if admin.role != "admin":
        return jsonify({
            "message": "Only Admin Can Update Staff"
        }), 403

    staff = User.query.get(staff_id)

    if not staff or staff.role != "staff":
        return jsonify({
            "message": "Staff Not Found"
        }), 404

    staff.active = not staff.active

    db.session.commit()

    return jsonify({
        "message": "Staff Status Updated Successfully"
    }), 200
# -------------------- Dashboard Stats --------------------

@app.route("/stats", methods=["GET"])
@jwt_required()
def dashboard_stats():

    current_user = get_jwt_identity()

    user = User.query.get(int(current_user))

    if user.role != "admin":
        return jsonify({
            "message": "Only Admin Can View Stats"
        }), 403

    return jsonify({
        "total_treks": Trek.query.count(),
        "total_users": User.query.filter_by(role="user").count(),
        "total_staff": User.query.filter_by(role="staff").count(),
        "total_bookings": Booking.query.count()
    }), 200
# -------------------- Get Users --------------------

@app.route("/users", methods=["GET"])
@jwt_required()
def get_users():

    current_user = get_jwt_identity()

    admin = User.query.get(int(current_user))

    if admin.role != "admin":
        return jsonify({
            "message": "Only Admin Can View Users"
        }), 403

    users = User.query.filter_by(role="user").all()

    result = []

    for user in users:

        result.append({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "active": user.active
        })

    return jsonify(result), 200
# -------------------- Activate / Deactivate User --------------------

@app.route("/users/<int:user_id>", methods=["PUT"])
@jwt_required()
def update_user_status(user_id):

    current_user = get_jwt_identity()

    admin = User.query.get(int(current_user))

    if admin.role != "admin":
        return jsonify({
            "message": "Only Admin Can Update Users"
        }), 403

    user = User.query.get(user_id)

    if not user or user.role != "user":
        return jsonify({
            "message": "User Not Found"
        }), 404

    user.active = not user.active

    db.session.commit()

    return jsonify({
        "message": "User Status Updated Successfully"
    }), 200
# -------------------- Update Profile --------------------

@app.route("/profile", methods=["PUT"])
@jwt_required()
def update_profile():

    current_user = get_jwt_identity()

    user = User.query.get(int(current_user))

    if not user:
        return jsonify({
            "message": "User Not Found"
        }), 404

    data = request.get_json()
    if (
        not data.get("name") or
        not data.get("email")
    ):
        return jsonify({
            "message": "All Fields Are Required"
        }), 400
    existing_user = User.query.filter_by(
    email=data["email"]
    ).first()

    if existing_user and existing_user.id != user.id:
        return jsonify({
            "message": "Email Already Exists"
        }), 400

    user.name = data["name"]
    user.email = data["email"]

    db.session.commit()

    return jsonify({
        "message": "Profile Updated Successfully"
    }), 200
# -------------------- Export Booking History --------------------

@app.route("/export/bookings", methods=["GET"])
@jwt_required()
def export_bookings():

    from tasks import export_booking_history

    current_user = get_jwt_identity()

    task = export_booking_history.delay(
        int(current_user)
    )

    return jsonify({
        "message": "Export Started",
        "task_id": task.id
    }), 202
if __name__ == "__main__":
    app.run(debug=True)
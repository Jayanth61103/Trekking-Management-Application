from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import db, User, UserRole

admin_bp = Blueprint("admin", __name__)

# Admin - Create Staff
@admin_bp.route("/admin/create-staff", methods=["POST"])
@jwt_required()
def create_staff():

    # Logged in user
    user_id = int(get_jwt_identity())

    current_user = User.query.get(user_id)

    # Only Admin can access
    if current_user is None or current_user.role != UserRole.ADMIN:
        return jsonify({
            "message": "Access Denied. Only Admin can create Staff."
        }), 403

    # Read request data
    data = request.get_json()

    full_name = data.get("full_name")
    username = data.get("username")
    email = data.get("email")
    phone = data.get("phone")
    password = data.get("password")

    # Required field validation
    if not all([full_name, username, email, phone, password]):
        return jsonify({
            "message": "All fields are required."
        }), 400

    # Phone validation
    if len(phone) != 10 or not phone.isdigit():
        return jsonify({
            "message": "Phone number must contain exactly 10 digits."
        }), 400

    # Duplicate Username
    if User.query.filter_by(username=username).first():
        return jsonify({
            "message": "Username already exists."
        }), 409

    # Duplicate Email
    if User.query.filter_by(email=email).first():
        return jsonify({
            "message": "Email already exists."
        }), 409

    # Duplicate Phone
    if User.query.filter_by(phone=phone).first():
        return jsonify({
            "message": "Phone number already exists."
        }), 409

    # Create Staff
    staff = User(
        full_name=full_name,
        username=username,
        email=email,
        phone=phone,
        password=password,          # Later: Hash Password
        role=UserRole.STAFF
    )

    try:

        db.session.add(staff)
        db.session.commit()

        return jsonify({
            "message": "Staff account created successfully."
        }), 201

    except Exception as e:

        db.session.rollback()

        return jsonify({
            "message": "Unable to create Staff.",
            "error": str(e)
        }), 500
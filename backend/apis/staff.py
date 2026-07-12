from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import User, UserRole

staff_bp = Blueprint("staff", __name__)

# Staff Dashboard
@staff_bp.route("/staff/dashboard", methods=["GET"])
@jwt_required()
def staff_dashboard():

    user_id = int(get_jwt_identity())

    user = User.query.get(user_id)

    if user is None or user.role != UserRole.STAFF:
        return jsonify({
            "message": "Access Denied. Staff only."
        }), 403

    return jsonify({
        "message": f"Welcome {user.full_name}",
        "role": user.role.value
    }), 200

# Staff Profile
@staff_bp.route("/staff/profile", methods=["GET"])
@jwt_required()
def staff_profile():

    user_id = int(get_jwt_identity())

    user = User.query.get(user_id)

    if user is None or user.role != UserRole.STAFF:
        return jsonify({
            "message": "Access Denied."
        }), 403

    return jsonify({
        "id": user.id,
        "full_name": user.full_name,
        "username": user.username,
        "email": user.email,
        "phone": user.phone,
        "role": user.role.value
    }), 200
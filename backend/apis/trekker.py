from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import User, UserRole

trekker_bp = Blueprint("trekker", __name__)

# Trekker Dashboard
@trekker_bp.route("/trekker/dashboard", methods=["GET"])
@jwt_required()
def trekker_dashboard():

    user_id = int(get_jwt_identity())

    user = User.query.get(user_id)

    if user is None or user.role != UserRole.TREKKER:
        return jsonify({
            "message": "Access Denied. Trekkers only."
        }), 403

    return jsonify({
        "message": f"Welcome {user.full_name}",
        "role": user.role.value
    }), 200


# Trekker Profile
@trekker_bp.route("/trekker/profile", methods=["GET"])
@jwt_required()
def trekker_profile():

    user_id = int(get_jwt_identity())

    user = User.query.get(user_id)

    if user is None or user.role != UserRole.TREKKER:
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
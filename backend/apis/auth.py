from flask import Blueprint, request, jsonify
from models import db, User, UserRole, Trekker
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, get_jwt

from datetime import datetime, timezone

from redis_client import redis_client

auth_bp = Blueprint("auth", __name__)

# Registeration 
# User Registration
@auth_bp.route("/register", methods=["POST"])
def register():

    # Read JSON data from frontend
    data = request.get_json()

    # Extract User Details
    full_name = data.get("full_name")
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    phone = data.get("phone")

    # Validate Required Fields
    if not all([full_name, username, email, phone, password]):
        return jsonify({
            "message": "Full name, username, email, phone number and password are required."
        }), 400

    # Validate Phone Number
    if len(phone) != 10 or not phone.isdigit():
        return jsonify({
            "message": "Phone number must contain exactly 10 digits."
        }), 400

    # Check Duplicate Username
    if User.query.filter_by(username=username).first():
        return jsonify({
            "message": "Username already exists."
        }), 409

    # Check Duplicate Email
    if User.query.filter_by(email=email).first():
        return jsonify({
            "message": "Email already registered."
        }), 409

    # Check Duplicate Phone Number
    if User.query.filter_by(phone=phone).first():
        return jsonify({
            "message": "Phone number already registered."
        }), 409

    try:
        # Create User
        new_user = User(
            full_name=full_name,
            username=username,
            email=email,
            password=generate_password_hash(password),         
            phone=phone,
            role=UserRole.TREKKER
        )

        # Add User to Session
        db.session.add(new_user)

        # Generate User ID without committing
        db.session.flush()

        # Automatically Create Trekker Profile
        new_trekker = Trekker(
            user_id=new_user.id
        )

        # Add Trekker Profile
        db.session.add(new_trekker)

        # Save Everything
        db.session.commit()

        return jsonify({
            "message": "User registered successfully.",
            "user": {
                "user_uuid": new_user.user_uuid,
                "username": new_user.username,
                "email": new_user.email,
                "role": new_user.role.value
            }
        }), 201

    except Exception as e:
        db.session.rollback()

        return jsonify({
            "message": "Registration failed.",
            "error": str(e)
        }), 500

# Login Verification
@auth_bp.route("/login", methods=["POST"])
def login():
    # Read JSON data
    data = request.get_json(silent=True) or {}
    # Extract Login Details
    email = data.get("email")
    password = data.get("password")
    # Validate Required Fields
    if not email or not password:
        return jsonify({
            "message": "Email and Password are required."
        }), 400
    # Check whether User exists
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({
            "message": "User not found."
        }), 404
    # Verify Password
    if not user.check_password(password):
        return jsonify({
            "message": "Invalid Password."
        }), 401
    # Check whether User account is active
    if not user.is_active:
        return jsonify({
            "message": "Your account is inactive or suspended. Please contact the administrator."
        }), 403
    try:
        # Update Last Login Time
        user.last_login = datetime.utcnow()
        db.session.commit()
        # Generate JWT Token
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={
                "username": user.username,
                "role": user.role.value
            }
        )
        # Return Success Response
        return jsonify({
            "message": "Login Successful.",
            "access_token": access_token,
            "user": {
                "user_uuid": user.user_uuid,
                "full_name": user.full_name,
                "username": user.username,
                "email": user.email,
                "phone": user.phone,
                "role": user.role.value
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        print("LOGIN ERROR:", e)
        return jsonify({
            "message": "Login failed."
        }), 500

# Fetches Profile Details  
@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def get_profile():

    user_id = get_jwt_identity()

    user = db.session.get(User, int(user_id))

    if not user:
        return jsonify({
            "message": "User not found."
        }), 404

    return jsonify({
        "user": {
            "user_uuid": user.user_uuid,
            "full_name": user.full_name,
            "username": user.username,
            "email": user.email,
            "phone": user.phone,
            "role": user.role.value,
            "email_verified": user.email_verified,
            "phone_verified": user.phone_verified
        }
    }), 200

# Update Profile Details
@auth_bp.route("/profile", methods=["PUT"])
@jwt_required()
def update_profile():

    try:

        # Get Logged-in User
        user_id = get_jwt_identity()

        user = db.session.get(User, int(user_id))

        if not user:
            return jsonify({
                "message": "User not found."
            }), 404

        # Read JSON Data
        data = request.get_json()

        full_name = data.get("full_name")
        username = data.get("username")
        email = data.get("email")
        phone = data.get("phone")

        # Validate Required Fields
        if not all([full_name, username, email, phone]):
            return jsonify({
                "message": "All fields are required."
            }), 400

        # Validate Phone Number
        if len(phone) != 10 or not phone.isdigit():
            return jsonify({
                "message": "Phone number must contain exactly 10 digits."
            }), 400

        # Check Duplicate Username
        existing_username = User.query.filter(
            User.username == username,
            User.id != user.id
        ).first()

        if existing_username:
            return jsonify({
                "message": "Username already exists."
            }), 409

        # Check Duplicate Email
        existing_email = User.query.filter(
            User.email == email,
            User.id != user.id
        ).first()

        if existing_email:
            return jsonify({
                "message": "Email already registered."
            }), 409

        # Check Duplicate Phone Number
        existing_phone = User.query.filter(
            User.phone == phone,
            User.id != user.id
        ).first()

        if existing_phone:
            return jsonify({
                "message": "Phone number already registered."
            }), 409

        # Check whether Email or Phone changed
        email_changed = (user.email != email)
        phone_changed = (user.phone != phone)

        # Update User Details
        user.full_name = full_name
        user.username = username
        user.email = email
        user.phone = phone

        # Reset Verification Status
        if email_changed:
            user.email_verified = False

        if phone_changed:
            user.phone_verified = False

        db.session.commit()
        return jsonify({
            "message": "Profile updated successfully.",
            "user": {
                "user_uuid": user.user_uuid,
                "full_name": user.full_name,
                "username": user.username,
                "email": user.email,
                "phone": user.phone,
                "role": user.role.value
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "message": "Failed to update profile.",
            "error": str(e)
        }), 500

# Change Password 
@auth_bp.route("/change-password", methods=["PUT"])
@jwt_required()
def change_password():

    try:

        # Get User ID from JWT
        user_id = get_jwt_identity()

        # Fetch Logged-in User
        user = db.session.get(User, int(user_id))

        if not user:
            return jsonify({
                "message": "User not found."
            }), 404

        # Read JSON Data
        data = request.get_json()

        current_password = data.get("current_password")
        new_password = data.get("new_password")
        confirm_password = data.get("confirm_password")

        # Validate Required Fields
        if not current_password or not new_password or not confirm_password:
            return jsonify({
                "message": "All password fields are required."
            }), 400

        # Check Current Password
        if not user.check_password(current_password):
            return jsonify({
                "message": "Current password is incorrect."
            }), 401

        # Check New Password Confirmation
        if new_password != confirm_password:
            return jsonify({
                "message": "New password and Confirm password do not match."
            }), 400

        # Prevent Same Password
        if current_password == new_password:
            return jsonify({
                "message": "New password cannot be the same as the current password."
            }), 400

        # Update Password
        user.set_password(new_password)

        db.session.commit()

        return jsonify({
            "message": "Password updated successfully."
        }), 200

    except Exception as e:

        db.session.rollback()

        return jsonify({
            "message": "Failed to update password.",
            "error": str(e)
        }), 500

# Logout User
@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():

    try:
        # Get Current JWT
        jwt_data = get_jwt()

        # Unique Token Identifier
        jti = jwt_data["jti"]

        # Token Expiration Time
        exp = jwt_data["exp"]

        # Current UTC Time
        now = datetime.now(timezone.utc).timestamp()

        # Remaining Token Lifetime
        expires_in = max(int(exp - now), 1)

        # Store Revoked Token in Redis
        redis_client.setex(jti, expires_in, "revoked")

        return jsonify({
            "message": "Logout successful. Token revoked."
        }), 200

    except Exception as e:
        return jsonify({
            "message": "Logout failed.",
            "error": str(e)
        }), 500
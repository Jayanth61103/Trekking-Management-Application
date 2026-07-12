from flask import Blueprint, request, jsonify
from models import db, User, UserRole
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, get_jwt

from datetime import datetime, timezone

from redis_client import redis_client

auth_bp = Blueprint("auth", __name__)

# Registeration 
@auth_bp.route("/register", methods=["POST"])
def register():

    # Read JSON data sent from frontend
    data = request.get_json()

    # Extract fields
    full_name = data.get("full_name")
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    phone = data.get("phone")

    # Default every new user as Trekker
    role = UserRole.TREKKER

    # Validate required fields
    if not full_name or not username or not email or not phone or not password:
        return jsonify({
            "message": "Full name, username, email and password are required."
        }), 400
    
    # Checks whether phone number has exactly 10 digits
    if len(phone) != 10 or not phone.isdigit():
        return jsonify({
            "message": "Phone number must contain exactly 10 digits."
    }), 400

    # Check duplicate username
    existing_username = User.query.filter_by(username=username).first()

    if existing_username:
        return jsonify({
            "message": "Username already exists."
        }), 409

    # Check duplicate email
    existing_email = User.query.filter_by(email=email).first()

    if existing_email:
        return jsonify({
            "message": "Email already registered."
        }), 409
    
    # Check duplicate Phone Number
    existing_phone = User.query.filter_by(phone=phone).first()

    if existing_phone:
        return jsonify({
            "message": "Phone number already registered."
    }), 409

    # Create User object
    new_user = User(
        full_name=full_name,
        username=username,
        email=email,
        password=password, 
        phone=phone,
        role=UserRole.TREKKER
    )

    try:
        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            "message": "User registered successfully."
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

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({
            "message": "Email and Password are required."
        }), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({
            "message": "User not found."
        }), 404

    if user.password != password:
        return jsonify({
            "message": "Invalid Password."
        }), 401
    
    # Password is correct
    access_token = create_access_token(
       identity=str(user.id),
       additional_claims={
         "username": user.username,
         "role": user.role.value
        }
    )

    return jsonify({
        "message": "Login Successful",
        "access_token": access_token, # Creates a JWT when registered user log-in 
        "user":{
            "id":user.id,
            "username":user.username,
            "email":user.email,
            "role":user.role.value
        }
    }), 200

# Checks profile with the JWT generated when logged-in
@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    try:
        # Get User ID from JWT
        user_id = get_jwt_identity()

        # Fetch User from Database
        user = db.session.get(User, int(user_id))

        # Check whether user exists
        if not user:
            return jsonify({
                "message": "User not found."
            }), 404

        # Return User Details
        return jsonify({
            "id": user.id,
            "full_name": user.full_name,
            "username": user.username,
            "email": user.email,
            "phone": user.phone,
            "role": user.role.value,
            "is_active": user.is_active

        }), 200

    except Exception as e:
        return jsonify({
            "message": "Failed to fetch user profile.",
            "error": str(e)
        }), 500

# Update Profile Details
@auth_bp.route("/profile", methods=["PUT"])
@jwt_required()
def update_profile():

    try:

        # Get Logged-in User ID
        user_id = get_jwt_identity()

        # Fetch User
        user = db.session.get(User, int(user_id))

        if not user:
            return jsonify({
                "message": "User not found."
            }), 404

        # Read JSON
        data = request.get_json()

        full_name = data.get("full_name")
        username = data.get("username")
        email = data.get("email")
        phone = data.get("phone")

        # Required Field Validation
        if not full_name or not username or not email or not phone:
            return jsonify({
                "message": "All fields are required."
            }), 400

        # Phone Validation
        if len(phone) != 10 or not phone.isdigit():
            return jsonify({
                "message": "Phone number must contain exactly 10 digits."
            }), 400

        # Username Validation
        existing_username = User.query.filter(
            User.username == username,
            User.id != user.id
        ).first()

        if existing_username:
            return jsonify({
                "message": "Username already exists."
            }), 409

        # Email Validation
        existing_email = User.query.filter(
            User.email == email,
            User.id != user.id
        ).first()

        if existing_email:
            return jsonify({
                "message": "Email already registered."
            }), 409

        # Phone Validation
        existing_phone = User.query.filter(
            User.phone == phone,
            User.id != user.id
        ).first()

        if existing_phone:
            return jsonify({
                "message": "Phone number already registered."
            }), 409

        # Update Details
        user.full_name = full_name
        user.username = username
        user.email = email
        user.phone = phone

        db.session.commit()

        return jsonify({
            "message": "Profile updated successfully."
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
        if user.password != current_password:
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
        user.password = new_password

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

    # Current JWT information
    jwt_data = get_jwt()

    # Unique Token ID
    jti = jwt_data["jti"]

    # Expiration Time
    exp = jwt_data["exp"]

    # Current UTC Time
    now = datetime.now(timezone.utc).timestamp()

    # Remaining lifetime of the token
    expires_in = max(int(exp - now), 1)

    # Store token ID in Redis until it naturally expires
    redis_client.setex(jti, expires_in, "revoked")

    return jsonify({
        "message": "Logout Successful. Token Revoked."
    }), 200
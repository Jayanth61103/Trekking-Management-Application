from flask import Blueprint, request, jsonify
from models import db, User, UserRole
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token

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
    if not full_name or not username or not email or not password:
        return jsonify({
            "message": "Full name, username, email and password are required."
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

    # Create User object
    new_user = User(
        full_name=full_name,
        username=username,
        email=email,
        password=password, 
        phone=phone,
        role=role
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
        "user": {
            "id": user.id,
            "username": user.username,
            "role": user.role.value
        }
    }), 200

# Checks profile with the JWT generated when logged-in
@auth_bp.route("/profile")
@jwt_required()
def profile():

    user_id = get_jwt_identity()

    user = User.query.get(user_id)

    return jsonify({
        "email": user.email,
        "username": user.username
    })
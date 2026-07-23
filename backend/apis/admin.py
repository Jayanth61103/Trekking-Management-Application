from datetime import date

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import (
    db,
    User,
    Staff,
    UserRole,
    Department,
    Designation,
    StaffStatus
)

from utils.mail import send_staff_welcome_email

admin_bp = Blueprint("admin", __name__)

# Admin - Create Staff
@admin_bp.route("/admin/create-staff", methods=["POST"])
@jwt_required()
def create_staff():

    # Get Logged-in User
    user_id = int(get_jwt_identity())

    current_user = db.session.get(User, user_id)

    # Only Admin can Create Staff
    if current_user is None or current_user.role != UserRole.ADMIN:
        return jsonify({
            "message": "Access denied. Only Admin can create Staff."
        }), 403

    # Read JSON Data
    data = request.get_json()

    full_name = data.get("full_name")
    username = data.get("username")
    email = data.get("email")
    phone = data.get("phone")
    password = data.get("password")

    department = data.get("department")
    designation = data.get("designation")

    # Validate Required Fields
    if not all([
        full_name,
        username,
        email,
        phone,
        password,
        department,
        designation
    ]):
        return jsonify({
            "message": "All fields are required."
        }), 400

    # Validate Phone Number
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

    try:
        # Create User
        new_user = User(
            full_name=full_name,
            username=username,
            email=email,
            phone=phone,
            password=password,
            role=UserRole.STAFF
        )

        db.session.add(new_user)

        # Generate User ID
        db.session.flush()

        # Generate Employee Code
        last_staff = Staff.query.order_by(Staff.staff_id.desc()).first()

        if last_staff:
            employee_code = f"EMP{last_staff.staff_id + 1:04d}"
        else:
            employee_code = "EMP0001"

        # Create Staff Profile
        new_staff = Staff(
            user_id=new_user.id,
            employee_code=employee_code,
            department=Department[department],
            designation=Designation[designation],
            joining_date=date.today(),
            experience_years=0,
            status=StaffStatus.ACTIVE
        )

        db.session.add(new_staff)
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "message": "Unable to create Staff.",
            "error": str(e)
        }), 500

    # Send Welcome Email
    try:
        send_staff_welcome_email(
            user_email=new_user.email,
            full_name=new_user.full_name,
            username=new_user.username,
            password=password
        )

    except Exception as e:
        return jsonify({
            "message": "Staff account created successfully, but email could not be sent.",
            "email_error": str(e)
        }), 201

    return jsonify({
        "message": "Staff account created successfully.",
        "staff": {
            "staff_uuid": new_staff.staff_uuid,
            "employee_code": new_staff.employee_code,
            "username": new_user.username,
            "email": new_user.email,
            "department": new_staff.department.value,
            "designation": new_staff.designation.value
        }
    }), 201
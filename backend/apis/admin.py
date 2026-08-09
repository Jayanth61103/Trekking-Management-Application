from datetime import date, datetime

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from werkzeug.security import generate_password_hash

from utils.cache import clear_cache_prefix

from models import (
    db,
    User,
    Staff,
    Trek,
    Trekker,
    Booking,
    UserRole,
    Department,
    Designation,
    StaffStatus,
    TrekDifficulty,
    TrekStatus,
    TrekkerStatus,
)

from utils.dashboard import get_dashboard_statistics
from utils.mail import send_staff_welcome_email

admin_bp = Blueprint("admin", __name__)

# Admin Dashboard
@admin_bp.route("/dashboard", methods=["GET"])
@jwt_required()
def dashboard():

    try:
        user_id = int(get_jwt_identity())

        current_user = db.session.get(
            User,
            user_id
        )
        if (
            current_user is None
            or current_user.role != UserRole.ADMIN
        ):
            return jsonify({
                "message":
                    "Access denied. Only Admin can access dashboard."
            }), 403
        statistics = get_dashboard_statistics()
        return jsonify({
            "statistics": statistics,
            "activities": []
        }), 200
    except Exception as e:
        print(
            "DASHBOARD ERROR:",
            repr(e)
        )
        return jsonify({
            "message":
                "Unable to load dashboard."
        }), 500

# Admin - Staff
@admin_bp.route("/create-staff", methods=["POST"])
@jwt_required()
def create_staff():
    # Check logged-in Admin
    user_id = int(get_jwt_identity())
    current_user = db.session.get(User, user_id)

    if current_user is None or current_user.role != UserRole.ADMIN:
        return jsonify({
            "message": "Access denied. Only Admin can create Staff."
        }), 403

    # Read request data
    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "message": "Request body must contain JSON data."
        }), 400

    full_name = str(data.get("full_name", "")).strip()
    username = str(data.get("username", "")).strip()
    email = str(data.get("email", "")).strip().lower()
    phone = str(data.get("phone", "")).strip()
    password = data.get("password", "")
    department_value = str(data.get("department", "")).strip().upper()
    designation_value = str(data.get("designation", "")).strip().upper()
    joining_date_value = data.get("joining_date")
    experience_years = data.get("experience_years", 0)

    # Validate required fields
    if not all([
        full_name, username, email, phone, password,
        department_value, designation_value
    ]):
        return jsonify({
            "message": "All required fields must be provided."
        }), 400

    if len(phone) != 10 or not phone.isdigit():
        return jsonify({
            "message": "Phone number must contain exactly 10 digits."
        }), 400

    # Validate experience
    try:
        experience_years = int(experience_years)

        if experience_years < 0:
            return jsonify({
                "message": "Experience years cannot be negative."
            }), 400

    except (ValueError, TypeError):
        return jsonify({
            "message": "Experience years must be a valid number."
        }), 400

    # Validate Department and Designation
    try:
        department = Department[department_value]
    except KeyError:
        return jsonify({
            "message": "Invalid Department.",
            "allowed_departments": [item.name for item in Department]
        }), 400

    try:
        designation = Designation[designation_value]
    except KeyError:
        return jsonify({
            "message": "Invalid Designation.",
            "allowed_designations": [item.name for item in Designation]
        }), 400

    # Validate joining date
    if joining_date_value:
        try:
            joining_date = date.fromisoformat(str(joining_date_value))
        except ValueError:
            return jsonify({
                "message": "Joining date must be in YYYY-MM-DD format."
            }), 400
    else:
        joining_date = date.today()

    # Check duplicate User information
    if User.query.filter_by(username=username).first():
        return jsonify({
            "message": "Username already exists."
        }), 409

    if User.query.filter_by(email=email).first():
        return jsonify({
            "message": "Email already exists."
        }), 409

    if User.query.filter_by(phone=phone).first():
        return jsonify({
            "message": "Phone number already exists."
        }), 409

    # Create User and Staff
    try:
        new_user = User(
            full_name=full_name,
            username=username,
            email=email,
            phone=phone,
            password=generate_password_hash(password),
            role=UserRole.STAFF,
            is_active=True
        )

        db.session.add(new_user)
        db.session.flush()

        last_staff = Staff.query.order_by(Staff.staff_id.desc()).first()

        if last_staff:
            employee_code = f"EMP{last_staff.staff_id + 1:04d}"
        else:
            employee_code = "EMP0001"

        new_staff = Staff(
            user_id=new_user.id,
            employee_code=employee_code,
            department=department,
            designation=designation,
            joining_date=joining_date,
            experience_years=experience_years,
            status=StaffStatus.ACTIVE
        )

        db.session.add(new_staff)
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        print("CREATE STAFF DATABASE ERROR:", repr(e))

        return jsonify({
            "message": "Unable to create Staff.",
            "error": str(e)
        }), 500

    # Send welcome email
    email_sent = True
    email_error = None

    try:
        send_staff_welcome_email(
            user_email=new_user.email,
            full_name=new_user.full_name,
            username=new_user.username,
            password=password
        )
    except Exception as e:
        email_sent = False
        email_error = str(e)
        print("STAFF WELCOME EMAIL ERROR:", repr(e))

    # Prepare response
    staff_data = {
        "staff_uuid": new_staff.staff_uuid,
        "employee_code": new_staff.employee_code,
        "full_name": new_user.full_name,
        "username": new_user.username,
        "email": new_user.email,
        "phone": new_user.phone,
        "department": new_staff.department.value,
        "designation": new_staff.designation.value,
        "joining_date": new_staff.joining_date.isoformat(),
        "experience_years": new_staff.experience_years,
        "status": new_staff.status.value
    }

    if not email_sent:
        return jsonify({
            "message": "Staff account created successfully, but welcome email could not be sent.",
            "email_error": email_error,
            "staff": staff_data
        }), 201

    return jsonify({
        "message": "Staff account created successfully.",
        "staff": staff_data
    }), 201

# Admin - Get All Staff
@admin_bp.route("/staff", methods=["GET"])
@jwt_required()
def get_all_staff():

    try:
        # Get logged-in user
        user_id = int(get_jwt_identity())
        current_user = db.session.get(User, user_id)

        # Only Admin can access
        if current_user is None or current_user.role != UserRole.ADMIN:
            return jsonify({
                "message": "Access denied. Only Admin can view Staff."
            }), 403

        # Get all Staff
        staff_list = Staff.query.order_by(Staff.staff_id.desc()).all()

        # Convert database objects into JSON
        staff_data = []

        for staff in staff_list:
            staff_data.append({
                "staff_uuid": staff.staff_uuid,
                "employee_code": staff.employee_code,
                "full_name": staff.user.full_name,
                "username": staff.user.username,
                "email": staff.user.email,
                "phone": staff.user.phone,
                "department": staff.department.value,
                "designation": staff.designation.value,
                "joining_date": (
                    staff.joining_date.isoformat()
                    if staff.joining_date
                    else None
                ),
                "experience_years": staff.experience_years,
                "status": staff.status.value
            })
        return jsonify({
            "staff": staff_data,
            "total": len(staff_data)
        }), 200

    except Exception as e:
        print(e)
        return jsonify({
            "message": "Unable to load Staff."
        }), 500

# Admin - Get Staff Details
@admin_bp.route("/staff/<staff_uuid>", methods=["GET"])
@jwt_required()
def get_staff_details(staff_uuid):
    try:
        # Logged-in User
        user_id = int(get_jwt_identity())
        current_user = db.session.get(User, user_id)

        # Admin Check
        if current_user is None or current_user.role != UserRole.ADMIN:
            return jsonify({
                "message": "Access denied."
            }), 403
        # Find Staff
        staff = Staff.query.filter_by(
            staff_uuid=staff_uuid
        ).first()
        if not staff:
            return jsonify({
                "message": "Staff not found."
            }), 404

        # Response
        return jsonify({
            "staff": {
                "staff_uuid": staff.staff_uuid,
                "employee_code": staff.employee_code,
                "full_name": staff.user.full_name,
                "username": staff.user.username,
                "email": staff.user.email,
                "phone": staff.user.phone,
                "department": staff.department.value,
                "designation": staff.designation.value,
                "joining_date": (
                    staff.joining_date.isoformat()
                    if staff.joining_date
                    else None
                ),
                "experience_years":
                    staff.experience_years,
                "status":
                    staff.status.value,
                "is_active":
                    staff.user.is_active
            }
        }), 200
    except Exception as e:
        print("Get Staff Details Error:", e)
        return jsonify({
            "message": "Unable to load Staff details."
        }), 500

# Admin - Update Staff Status
@admin_bp.route("/staff/<staff_uuid>/status", methods=["PATCH"])
@jwt_required()
def update_staff_status(staff_uuid):
    try:
        # Get Logged-in Admin
        user_id = int(get_jwt_identity())
        current_user = db.session.get(User, user_id)
        # Admin Check
        if current_user is None or current_user.role != UserRole.ADMIN:
            return jsonify({
                "message": "Access denied. Only Admin can update Staff status."
            }), 403
        # Find Staff
        staff = Staff.query.filter_by(
            staff_uuid=staff_uuid
        ).first()
        if not staff:
            return jsonify({
                "message": "Staff not found."
            }), 404
        # Read Request Data
        data = request.get_json() or {}
        status = data.get("status")
        if not status:
            return jsonify({
                "message": "Status is required."
            }), 400
        # Validate Status
        try:
            new_status = StaffStatus[status.upper()]
        except KeyError:
            return jsonify({
                "message": "Invalid Staff status."
            }), 400
        # Dismissed Staff cannot be reactivated
        if staff.status == StaffStatus.DISMISSED:
            return jsonify({
                "message": "Dismissed Staff status cannot be changed."
            }), 400
        # Update Staff Status
        staff.status = new_status
        # Control User Login Access
        if new_status == StaffStatus.ACTIVE:
            staff.user.is_active = True
        else:
            staff.user.is_active = False
        db.session.commit()
        return jsonify({
            "message": "Staff status updated successfully.",
            "staff": {
                "staff_uuid": staff.staff_uuid,
                "employee_code": staff.employee_code,
                "full_name": staff.user.full_name,
                "status": staff.status.value,
                "is_active": staff.user.is_active
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        print("Update Staff Status Error:", e)
        return jsonify({
            "message": "Unable to update Staff status."
        }), 500

# Admin - Get Eligible Guides
@admin_bp.route("/eligible-guides", methods=["GET"])
@jwt_required()
def get_eligible_guides():
    try:
        # Get logged-in User ID from JWT
        user_id = int(get_jwt_identity())
        # Get logged-in User
        current_user = db.session.get(
            User,
            user_id
        )
        # Only Admin can access
        if (
            current_user is None
            or current_user.role != UserRole.ADMIN):
            return jsonify({
                "message":
                    "Access denied. Only Admin can view eligible Guides."
            }), 403

        # Get only Active Guides
        eligible_guides = Staff.query.filter(
            Staff.designation == Designation.GUIDE,
            Staff.status == StaffStatus.ACTIVE
        ).all()

        # Prepare Response
        guides_data = []
        for guide in eligible_guides:
            # User account must also be active
            if (
                guide.user is not None
                and guide.user.is_active
            ):
                guides_data.append({
                    "staff_uuid":
                        guide.staff_uuid,

                    "employee_code":
                        guide.employee_code,

                    "full_name":
                        guide.user.full_name,

                    "email":
                        guide.user.email,

                    "designation":
                        guide.designation.value,

                    "status":
                        guide.status.value
                })
        return jsonify({
            "guides": guides_data,
            "total": len(guides_data)
        }), 200
    except Exception as e:
        print(
            "GET ELIGIBLE GUIDES ERROR:",e
        )
        return jsonify({
            "message":
                "Unable to load eligible Guides.",
            "error":
                str(e)
        }), 500

# ADMIN - CREATE TREK
@admin_bp.route("/create-trek", methods=["POST"])
@jwt_required()
def create_trek():
    try:
        # Get Logged-in User
        user_id = int(get_jwt_identity())
        current_user = db.session.get(
            User,
            user_id
        )

        # Admin Authorization
        if (
            current_user is None
            or current_user.role != UserRole.ADMIN):
            return jsonify({
                "message":
                    "Access denied. Only Admin can create Treks."
            }), 403

        # Read Request Data
        data = request.get_json() or {}

        staff_uuid = data.get("staff_uuid")
        trek_name = data.get("trek_name")
        location = data.get("location")
        difficulty = data.get("difficulty")
        capacity = data.get("capacity")
        price = data.get("price")
        start_date = data.get("start_date")
        end_date = data.get("end_date")
        description = data.get("description")
        meeting_point = data.get("meeting_point")

        # Validate Required Fields
        if not all([
            staff_uuid,
            trek_name,
            location,
            difficulty,
            capacity,
            price,
            start_date,
            end_date,
            description]):
            
            return jsonify({
                "message":
                    "All required Trek fields must be provided."
            }), 400

        # Find Assigned Staff
        staff = Staff.query.filter_by(
            staff_uuid=staff_uuid
        ).first()

        if not staff:
            return jsonify({
                "message":
                    "Selected Staff not found."
            }), 404

        # Check Staff Employment Status
        if staff.status != StaffStatus.ACTIVE:
            return jsonify({
                "message":
                    "Only Active Staff can be assigned to a Trek."
            }), 400

        # Check User Account Status
        if not staff.user.is_active:
            return jsonify({
                "message":
                    "This Staff account is inactive and cannot "
                    "be assigned to a Trek."
            }), 400

        # Only Guides can be Assigned
        if staff.designation != Designation.GUIDE:
            return jsonify({
                "message":
                    "Only Staff with Guide designation can "
                    "be assigned to a Trek."
            }), 400

        # Validate Trek Difficulty
        try:
            trek_difficulty = TrekDifficulty[
                difficulty.upper()]
        except (KeyError, AttributeError):
            return jsonify({
                "message":
                    "Difficulty must be Easy, Moderate, "
                    "Difficult or Extreme."
            }), 400

        # Convert Dates
        try:
            trek_start_date = datetime.strptime(
                start_date,
                "%Y-%m-%d"
            ).date()
            trek_end_date = datetime.strptime(
                end_date,
                "%Y-%m-%d"
            ).date()
        except (ValueError, TypeError):
            return jsonify({
                "message":
                    "Start date and End date must use "
                    "YYYY-MM-DD format."
            }), 400

        # Validate Date Range
        if trek_end_date < trek_start_date:
            return jsonify({
                "message":
                    "End date cannot be before Start date."
            }), 400

        # Validate Capacity
        try:
            capacity = int(capacity)
            if capacity <= 0:
                return jsonify({
                    "message":
                        "Capacity must be greater than 0."
                }), 400
        except (ValueError, TypeError):
            return jsonify({
                "message":
                    "Capacity must be a valid whole number."
            }), 400


        # Validate Price
        try:
            price = float(price)

            if price < 0:
                return jsonify({
                    "message":
                        "Price cannot be negative."
                }), 400
        except (ValueError, TypeError):
            return jsonify({
                "message":
                    "Price must be a valid number."
            }), 400

        # Calculate Duration Automatically
        duration_days = (
            trek_end_date - trek_start_date
        ).days + 1

        # Create Trek
        new_trek = Trek(
            staff_id=staff.staff_id,
            trek_name=trek_name.strip(),
            location=location.strip(),
            duration_days=duration_days,
            difficulty=trek_difficulty,
            capacity=capacity,
            # Initially no bookings exist
            available_slots=capacity,
            price=price,
            start_date=trek_start_date,
            end_date=trek_end_date,
            description=description.strip(),
            meeting_point=(
                meeting_point.strip()
                if meeting_point
                else None
            ),
            status=TrekStatus.UPCOMING
        )

        # Save Trek
        db.session.add(new_trek)
        db.session.commit()

        # Clear cached trek listings since a new Trek now exists
        clear_cache_prefix("treks:")

        # Success Response
        return jsonify({
            "message":
                "Trek created successfully.",
            "trek": {
                "trek_uuid":
                    new_trek.trek_uuid,
                "trek_name":
                    new_trek.trek_name,
                "location":
                    new_trek.location,
                "duration_days":
                    new_trek.duration_days,
                "difficulty":
                    new_trek.difficulty.value,
                "capacity":
                    new_trek.capacity,
                "available_slots":
                    new_trek.available_slots,
                "price":
                    float(new_trek.price),
                "start_date":
                    new_trek.start_date.isoformat(),
                "end_date":
                    new_trek.end_date.isoformat(),
                "status":
                    new_trek.status.value,
                "description":
                    new_trek.description,
                "meeting_point":
                    new_trek.meeting_point,
                "assigned_staff": {
                    "staff_uuid":
                        staff.staff_uuid,
                    "employee_code":
                        staff.employee_code,
                    "full_name":
                        staff.user.full_name,
                    "designation":
                        staff.designation.value,
                    "status":
                        staff.status.value
                }
            }
        }), 201
    except Exception as e:
        # Undo any unfinished database operation
        db.session.rollback()
        print(
            "Create Trek Error:",
            e
        )
        return jsonify({
            "message":
                "Unable to create Trek."
        }), 500

# Admin - Get All Treks
@admin_bp.route("/treks", methods=["GET"])
@jwt_required()
def get_all_treks():
    try:
        # Get Logged-in User
        user_id = int(get_jwt_identity())
        current_user = db.session.get(User, user_id)

        # Only Admin can view all Treks
        if current_user is None or current_user.role != UserRole.ADMIN:
            return jsonify({
                "message": "Access denied. Only Admin can view Treks."
            }), 403
        # Get all Treks
        trek_list = Trek.query.order_by(
            Trek.start_date.desc()
        ).all()
        trek_data = []
        for trek in trek_list:
            trek_data.append({
                "trek_id": trek.trek_id,
                "trek_uuid": trek.trek_uuid,
                "trek_name": trek.trek_name,
                "location": trek.location,
                "duration_days": trek.duration_days,
                "difficulty": trek.difficulty.value,
                "capacity": trek.capacity,
                "available_slots": trek.available_slots,
                "price": float(trek.price),
                "start_date": trek.start_date.isoformat(),
                "end_date": trek.end_date.isoformat(),
                "status": trek.status.value,

                "assigned_guide": {
                    "staff_uuid": trek.staff.staff_uuid,
                    "employee_code": trek.staff.employee_code,
                    "full_name": trek.staff.user.full_name
                }
            })
        return jsonify({
            "treks": trek_data,
            "total": len(trek_data)
        }), 200
    except Exception as e:
        print("GET ALL TREKS ERROR:", repr(e))
        return jsonify({
            "message": "Unable to load Treks."
        }), 500

# Admin - Get Trek Details
@admin_bp.route("/treks/<trek_uuid>", methods=["GET"])
@jwt_required()
def get_trek_details(trek_uuid):

    try:
        # Get Logged-in User
        user_id = int(get_jwt_identity())

        current_user = db.session.get(User, user_id)

        # Only Admin can Access Trek Details
        if current_user is None or current_user.role != UserRole.ADMIN:
            return jsonify({
                "message": "Access denied. Only Admin can view Trek details."
            }), 403

        # Find Trek using Trek UUID
        trek = Trek.query.filter_by(
            trek_uuid=trek_uuid
        ).first()

        # Check whether Trek exists
        if not trek:
            return jsonify({
                "message": "Trek not found."
            }), 404

        # Assigned Staff Details
        assigned_staff = None

        if trek.staff:
            assigned_staff = {
                "staff_uuid": trek.staff.staff_uuid,
                "employee_code": trek.staff.employee_code,
                "full_name": trek.staff.user.full_name
            }

        # Return Trek Details
        return jsonify({
            "trek": {
                "trek_uuid": trek.trek_uuid,
                "trek_id": trek.trek_id,
                "trek_name": trek.trek_name,
                "location": trek.location,
                "duration_days": trek.duration_days,
                "difficulty": trek.difficulty.value,
                "capacity": trek.capacity,
                "available_slots": trek.available_slots,
                "price": float(trek.price),
                "start_date": (
                    trek.start_date.isoformat()
                    if trek.start_date
                    else None
                ),
                "end_date": (
                    trek.end_date.isoformat()
                    if trek.end_date
                    else None
                ),
                "meeting_point": trek.meeting_point,
                "description": trek.description,
                "status": trek.status.value,
                "assigned_staff": assigned_staff
            }
        }), 200

    except Exception as e:

        print("Get Trek Details Error:", e)

        return jsonify({
            "message": "Unable to load Trek details.",
            "error": str(e)
        }), 500
    
# Admin - Update Trek
@admin_bp.route("/treks/<trek_uuid>", methods=["PATCH"])
@jwt_required()
def update_trek(trek_uuid):
    try:
        # Get Logged-in User
        user_id = int(get_jwt_identity())
        current_user = db.session.get(User, user_id)

        # Only Admin can Update Treks
        if current_user is None or current_user.role != UserRole.ADMIN:
            return jsonify({
                "message": "Access denied. Only Admin can update Treks."
            }), 403

        # Find Trek
        trek = Trek.query.filter_by(
            trek_uuid=trek_uuid
        ).first()

        if trek is None:
            return jsonify({
                "message": "Trek not found."
            }), 404

        # Read Request Data
        data = request.get_json(silent=True)

        if not data:
            return jsonify({
                "message": "No update data provided."
            }), 400
        # Update Trek Name
        if "trek_name" in data:
            trek_name = str(data["trek_name"]).strip()

            if not trek_name:
                return jsonify({
                    "message": "Trek name cannot be empty."
                }), 400

            trek.trek_name = trek_name
        # Update Location
        if "location" in data:
            trek.location = str(data["location"]).strip()
        # Update Capacity
        if "capacity" in data:
            new_capacity = int(data["capacity"])

            if new_capacity <= 0:
                return jsonify({
                    "message": "Capacity must be greater than 0."
                }), 400

            # Calculate currently occupied slots
            booked_slots = trek.capacity - trek.available_slots

            # Capacity cannot be lower than existing bookings
            if new_capacity < booked_slots:
                return jsonify({
                    "message":
                    f"Capacity cannot be less than {booked_slots} "
                    "because those slots are already occupied."
                }), 400

            trek.capacity = new_capacity

            # Preserve existing bookings while changing capacity
            trek.available_slots = new_capacity - booked_slots

        # Update Price
        if "price" in data:
            new_price = float(data["price"])

            if new_price < 0:
                return jsonify({
                    "message": "Price cannot be negative."
                }), 400

            trek.price = new_price
        # Update Meeting Point
        if "meeting_point" in data:
            trek.meeting_point = str(
                data["meeting_point"]
            ).strip()
        # Update Description
        if "description" in data:
            description = str(data["description"]).strip()

            if not description:
                return jsonify({
                    "message": "Description cannot be empty."
                }), 400

            trek.description = description
        # Update Difficulty
        if "difficulty" in data:
            try:
                trek.difficulty = TrekDifficulty[
                    str(data["difficulty"]).upper()
                ]

            except KeyError:
                return jsonify({
                    "message": "Invalid Trek difficulty."
                }), 400
        # Update Status
        if "status" in data:
            try:
                trek.status = TrekStatus[
                    str(data["status"]).upper()
                ]

            except KeyError:
                return jsonify({
                    "message": "Invalid Trek status."
                }), 400
        # Update Start Date
        if "start_date" in data:
            trek.start_date = date.fromisoformat(
                data["start_date"]
            )
        # Update End Date
        if "end_date" in data:
            trek.end_date = date.fromisoformat(
                data["end_date"]
            )
        # Validate Dates and Recalculate Duration
        if trek.start_date and trek.end_date:

            if trek.end_date < trek.start_date:
                return jsonify({
                    "message":
                    "End date cannot be before Start date."
                }), 400

            trek.duration_days = (
                trek.end_date - trek.start_date
            ).days + 1
        # Save Changes
        db.session.commit()

        # Clear cached trek listings since this Trek's details changed
        clear_cache_prefix("treks:")

        # Response
        return jsonify({
            "message": "Trek updated successfully.",

            "trek": {
                "trek_uuid": trek.trek_uuid,
                "trek_id": trek.trek_id,
                "trek_name": trek.trek_name,
                "location": trek.location,
                "difficulty": trek.difficulty.value,
                "duration_days": trek.duration_days,
                "capacity": trek.capacity,
                "available_slots": trek.available_slots,
                "price": float(trek.price),

                "start_date": (
                    trek.start_date.isoformat()
                    if trek.start_date
                    else None
                ),

                "end_date": (
                    trek.end_date.isoformat()
                    if trek.end_date
                    else None
                ),

                "meeting_point": trek.meeting_point,
                "description": trek.description,
                "status": trek.status.value
            }
        }), 200

    except ValueError as e:
        db.session.rollback()

        return jsonify({
            "message": "Invalid data provided.",
            "error": str(e)
        }), 400

    except Exception as e:
        db.session.rollback()

        print("Update Trek Error:", e)

        return jsonify({
            "message": "Unable to update Trek."
        }), 500

# Admin - Get All Trekkers
@admin_bp.route("/trekkers", methods=["GET"])
@jwt_required()
def get_all_trekkers():
    try:
        user_id = int(get_jwt_identity())
        current_user = db.session.get(User, user_id)

        if current_user is None or current_user.role != UserRole.ADMIN:
            return jsonify({
                "message": "Access denied. Only Admin can view Trekkers."
            }), 403

        trekkers = Trekker.query.order_by(Trekker.trekker_id.desc()).all()

        trekkers_data = []
        for trekker in trekkers:
            trekkers_data.append({
                "trekker_uuid": trekker.trekker_uuid,
                "user_uuid": trekker.user.user_uuid,
                "full_name": trekker.user.full_name,
                "username": trekker.user.username,
                "email": trekker.user.email,
                "phone": trekker.user.phone,
                "status": trekker.status.value,
                "is_active": trekker.user.is_active,
                "total_bookings": len(trekker.bookings)
            })

        return jsonify({
            "trekkers": trekkers_data,
            "total": len(trekkers_data)
        }), 200

    except Exception as e:
        print("GET ALL TREKKERS ERROR:", repr(e))
        return jsonify({
            "message": "Unable to load Trekkers."
        }), 500


# Admin - Get Trekker Details
@admin_bp.route("/trekkers/<trekker_uuid>", methods=["GET"])
@jwt_required()
def get_trekker_details(trekker_uuid):
    try:
        user_id = int(get_jwt_identity())
        current_user = db.session.get(User, user_id)

        if current_user is None or current_user.role != UserRole.ADMIN:
            return jsonify({
                "message": "Access denied."
            }), 403

        trekker = Trekker.query.filter_by(
            trekker_uuid=trekker_uuid
        ).first()

        if not trekker:
            return jsonify({
                "message": "Trekker not found."
            }), 404

        return jsonify({
            "trekker": {
                "trekker_uuid": trekker.trekker_uuid,
                "user_uuid": trekker.user.user_uuid,
                "full_name": trekker.user.full_name,
                "username": trekker.user.username,
                "email": trekker.user.email,
                "phone": trekker.user.phone,
                "date_of_birth": (
                    trekker.date_of_birth.isoformat()
                    if trekker.date_of_birth else None
                ),
                "gender": trekker.gender.value if trekker.gender else None,
                "blood_group": trekker.blood_group.value if trekker.blood_group else None,
                "emergency_contact": trekker.emergency_contact,
                "medical_conditions": trekker.medical_conditions,
                "status": trekker.status.value,
                "is_active": trekker.user.is_active,
                "total_bookings": len(trekker.bookings)
            }
        }), 200

    except Exception as e:
        print("Get Trekker Details Error:", e)
        return jsonify({
            "message": "Unable to load Trekker details."
        }), 500


# Admin - Update Trekker Status (Blacklist/Deactivate/Reactivate)
@admin_bp.route("/trekkers/<trekker_uuid>/status", methods=["PATCH"])
@jwt_required()
def update_trekker_status(trekker_uuid):
    try:
        user_id = int(get_jwt_identity())
        current_user = db.session.get(User, user_id)

        if current_user is None or current_user.role != UserRole.ADMIN:
            return jsonify({
                "message": "Access denied. Only Admin can update Trekkers."
            }), 403

        trekker = Trekker.query.filter_by(
            trekker_uuid=trekker_uuid
        ).first()

        if not trekker:
            return jsonify({
                "message": "Trekker not found."
            }), 404

        data = request.get_json() or {}
        status = data.get("status")

        if not status:
            return jsonify({
                "message": "Status is required."
            }), 400

        try:
            new_status = TrekkerStatus[status.upper()]
        except KeyError:
            return jsonify({
                "message": "Invalid Trekker status."
            }), 400

        trekker.status = new_status

        if new_status == TrekkerStatus.ACTIVE:
            trekker.user.is_active = True
        else:
            trekker.user.is_active = False

        db.session.commit()

        return jsonify({
            "message": "Trekker status updated successfully.",
            "trekker": {
                "trekker_uuid": trekker.trekker_uuid,
                "full_name": trekker.user.full_name,
                "status": trekker.status.value,
                "is_active": trekker.user.is_active
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        print("Update Trekker Status Error:", e)
        return jsonify({
            "message": "Unable to update Trekker status."
        }), 500

# Admin - Get All Bookings (History)
@admin_bp.route("/bookings", methods=["GET"])
@jwt_required()
def get_all_bookings():
    try:
        user_id = int(get_jwt_identity())
        current_user = db.session.get(User, user_id)

        if current_user is None or current_user.role != UserRole.ADMIN:
            return jsonify({
                "message": "Access denied. Only Admin can view Bookings."
            }), 403

        bookings = Booking.query.order_by(Booking.booking_date.desc()).all()

        bookings_data = []
        for booking in bookings:
            bookings_data.append({
                "booking_uuid": booking.booking_uuid,
                "trekker_name": booking.trekker.user.full_name,
                "trekker_email": booking.trekker.user.email,
                "trek_name": booking.trek.trek_name,
                "trek_uuid": booking.trek.trek_uuid,
                "number_of_people": booking.number_of_people,
                "booking_amount": float(booking.booking_amount),
                "booking_status": booking.booking_status.value,
                "payment_status": booking.payment_status.value,
                "booking_date": (
                    booking.booking_date.isoformat()
                    if booking.booking_date else None
                ),
                "trek_status": booking.trek.status.value
            })

        return jsonify({
            "bookings": bookings_data,
            "total": len(bookings_data)
        }), 200

    except Exception as e:
        print("GET ALL BOOKINGS ERROR:", repr(e))
        return jsonify({
            "message": "Unable to load Bookings."
        }), 500
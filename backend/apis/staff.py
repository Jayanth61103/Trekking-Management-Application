from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import (
    db,
    User,
    Staff,
    Trek,
    UserRole,
    TrekStatus,
    BookingStatus
)

staff_bp = Blueprint("staff", __name__)


def get_logged_in_staff(user_id):
    """Returns (user, staff) if the logged-in user is a valid Staff member, else (None, None)."""
    user = db.session.get(User, user_id)
    if user is None or user.role != UserRole.STAFF:
        return None, None
    staff = Staff.query.filter_by(user_id=user.id).first()
    return user, staff


# Staff Dashboard
@staff_bp.route("/dashboard", methods=["GET"])
@jwt_required()
def staff_dashboard():
    user_id = int(get_jwt_identity())
    user, staff = get_logged_in_staff(user_id)

    if user is None or staff is None:
        return jsonify({"message": "Access Denied. Staff only."}), 403

    assigned_treks = Trek.query.filter_by(staff_id=staff.staff_id).all()

    total_participants = 0
    open_treks = 0
    for trek in assigned_treks:
        total_participants += len(trek.bookings)
        if trek.status == TrekStatus.OPEN:
            open_treks += 1

    return jsonify({
        "full_name": user.full_name,
        "employee_code": staff.employee_code,
        "assigned_treks": len(assigned_treks),
        "total_participants": total_participants,
        "open_treks": open_treks
    }), 200


# Staff Profile
@staff_bp.route("/profile", methods=["GET"])
@jwt_required()
def staff_profile():
    user_id = int(get_jwt_identity())
    user, staff = get_logged_in_staff(user_id)

    if user is None or staff is None:
        return jsonify({"message": "Access Denied."}), 403

    return jsonify({
        "id": user.id,
        "full_name": user.full_name,
        "username": user.username,
        "email": user.email,
        "phone": user.phone,
        "role": user.role.value,
        "employee_code": staff.employee_code,
        "department": staff.department.value if staff.department else None,
        "designation": staff.designation.value if staff.designation else None
    }), 200


# Staff - Get My Assigned Treks
@staff_bp.route("/treks", methods=["GET"])
@jwt_required()
def get_my_treks():
    user_id = int(get_jwt_identity())
    user, staff = get_logged_in_staff(user_id)

    if user is None or staff is None:
        return jsonify({"message": "Access Denied. Staff only."}), 403

    treks = Trek.query.filter_by(
        staff_id=staff.staff_id
    ).order_by(Trek.start_date.desc()).all()

    treks_data = []
    for trek in treks:
        treks_data.append({
            "trek_id": trek.trek_id,
            "trek_uuid": trek.trek_uuid,
            "trek_name": trek.trek_name,
            "location": trek.location,
            "difficulty": trek.difficulty.value,
            "capacity": trek.capacity,
            "available_slots": trek.available_slots,
            "start_date": trek.start_date.isoformat(),
            "end_date": trek.end_date.isoformat(),
            "status": trek.status.value,
            "participants_count": len(trek.bookings)
        })

    return jsonify({
        "treks": treks_data,
        "total": len(treks_data)
    }), 200


# Staff - Get One Assigned Trek (with Participants)
@staff_bp.route("/treks/<trek_uuid>", methods=["GET"])
@jwt_required()
def get_my_trek_details(trek_uuid):
    user_id = int(get_jwt_identity())
    user, staff = get_logged_in_staff(user_id)

    if user is None or staff is None:
        return jsonify({"message": "Access Denied. Staff only."}), 403

    trek = Trek.query.filter_by(trek_uuid=trek_uuid).first()

    if not trek:
        return jsonify({"message": "Trek not found."}), 404

    # Ownership check — staff can only manage their own assigned treks
    if trek.staff_id != staff.staff_id:
        return jsonify({
            "message": "Access denied. This Trek is not assigned to you."
        }), 403

    participants = []
    for booking in trek.bookings:
        participants.append({
            "booking_uuid": booking.booking_uuid,
            "trekker_name": booking.trekker.user.full_name,
            "email": booking.trekker.user.email,
            "phone": booking.trekker.user.phone,
            "number_of_people": booking.number_of_people,
            "booking_status": booking.booking_status.value,
            "payment_status": booking.payment_status.value,
            "booking_date": (
                booking.booking_date.isoformat()
                if booking.booking_date else None
            )
        })

    return jsonify({
        "trek": {
            "trek_id": trek.trek_id,
            "trek_uuid": trek.trek_uuid,
            "trek_name": trek.trek_name,
            "location": trek.location,
            "difficulty": trek.difficulty.value,
            "capacity": trek.capacity,
            "available_slots": trek.available_slots,
            "start_date": trek.start_date.isoformat(),
            "end_date": trek.end_date.isoformat(),
            "status": trek.status.value,
            "description": trek.description,
            "meeting_point": trek.meeting_point
        },
        "participants": participants,
        "total_participants": len(participants)
    }), 200


# Staff - Update Available Slots
@staff_bp.route("/treks/<trek_uuid>/slots", methods=["PATCH"])
@jwt_required()
def update_trek_slots(trek_uuid):
    user_id = int(get_jwt_identity())
    user, staff = get_logged_in_staff(user_id)

    if user is None or staff is None:
        return jsonify({"message": "Access Denied. Staff only."}), 403

    trek = Trek.query.filter_by(trek_uuid=trek_uuid).first()

    if not trek:
        return jsonify({"message": "Trek not found."}), 404

    if trek.staff_id != staff.staff_id:
        return jsonify({
            "message": "Access denied. This Trek is not assigned to you."
        }), 403

    data = request.get_json() or {}
    available_slots = data.get("available_slots")

    if available_slots is None:
        return jsonify({"message": "available_slots is required."}), 400

    try:
        available_slots = int(available_slots)
    except (ValueError, TypeError):
        return jsonify({"message": "available_slots must be a valid number."}), 400

    if available_slots < 0:
        return jsonify({"message": "Available slots cannot be negative."}), 400

    if available_slots > trek.capacity:
        return jsonify({
            "message": f"Available slots cannot exceed capacity ({trek.capacity})."
        }), 400

    try:
        trek.available_slots = available_slots
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print("Update Trek Slots Error:", e)
        return jsonify({"message": "Unable to update slots."}), 500

    return jsonify({
        "message": "Trek slots updated successfully.",
        "trek": {
            "trek_uuid": trek.trek_uuid,
            "available_slots": trek.available_slots,
            "capacity": trek.capacity
        }
    }), 200


# Staff - Update Trek Status (Open / Completed / Cancelled)
@staff_bp.route("/treks/<trek_uuid>/status", methods=["PATCH"])
@jwt_required()
def update_trek_status(trek_uuid):
    user_id = int(get_jwt_identity())
    user, staff = get_logged_in_staff(user_id)

    if user is None or staff is None:
        return jsonify({"message": "Access Denied. Staff only."}), 403

    trek = Trek.query.filter_by(trek_uuid=trek_uuid).first()

    if not trek:
        return jsonify({"message": "Trek not found."}), 404

    if trek.staff_id != staff.staff_id:
        return jsonify({
            "message": "Access denied. This Trek is not assigned to you."
        }), 403

    data = request.get_json() or {}
    status = data.get("status")

    if not status:
        return jsonify({"message": "Status is required."}), 400

    try:
        new_status = TrekStatus[status.upper()]
    except KeyError:
        return jsonify({
            "message": "Invalid Trek status.",
            "allowed_statuses": [item.name for item in TrekStatus]
        }), 400

    if trek.status in [TrekStatus.COMPLETED, TrekStatus.CANCELLED]:
        return jsonify({
            "message": f"Trek is already {trek.status.value} and its status cannot be changed."
        }), 400

    trek.status = new_status

    # When a Trek is marked Completed, cascade to its approved bookings
    if new_status == TrekStatus.COMPLETED:
        for booking in trek.bookings:
            if booking.booking_status == BookingStatus.APPROVED:
                booking.booking_status = BookingStatus.COMPLETED

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print("Update Trek Status Error:", e)
        return jsonify({"message": "Unable to update Trek status."}), 500

    return jsonify({
        "message": "Trek status updated successfully.",
        "trek": {
            "trek_uuid": trek.trek_uuid,
            "status": trek.status.value
        }
    }), 200
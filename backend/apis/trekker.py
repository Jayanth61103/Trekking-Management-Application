from datetime import datetime

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import (
    db,
    User,
    Trekker,
    Trek,
    Booking,
    UserRole,
    TrekStatus,
    TrekDifficulty,
    BookingStatus,
    PaymentStatus
)

trekker_bp = Blueprint("trekker", __name__)


def get_logged_in_trekker(user_id):
    """Returns (user, trekker) if the logged-in user is a valid Trekker, else (None, None)."""
    user = db.session.get(User, user_id)
    if user is None or user.role != UserRole.TREKKER:
        return None, None
    trekker = Trekker.query.filter_by(user_id=user.id).first()
    return user, trekker


# Trekker Dashboard
@trekker_bp.route("/dashboard", methods=["GET"])
@jwt_required()
def trekker_dashboard():
    user_id = int(get_jwt_identity())
    user, trekker = get_logged_in_trekker(user_id)

    if user is None or trekker is None:
        return jsonify({"message": "Access Denied. Trekkers only."}), 403

    total_bookings = len(trekker.bookings)
    active_bookings = sum(
        1 for b in trekker.bookings
        if b.booking_status in [BookingStatus.PENDING, BookingStatus.APPROVED]
    )
    completed_treks = sum(
        1 for b in trekker.bookings
        if b.booking_status == BookingStatus.COMPLETED
    )

    return jsonify({
        "full_name": user.full_name,
        "total_bookings": total_bookings,
        "active_bookings": active_bookings,
        "completed_treks": completed_treks
    }), 200


# Trekker Profile
@trekker_bp.route("/profile", methods=["GET"])
@jwt_required()
def trekker_profile():
    user_id = int(get_jwt_identity())
    user, trekker = get_logged_in_trekker(user_id)

    if user is None or trekker is None:
        return jsonify({"message": "Access Denied."}), 403

    return jsonify({
        "id": user.id,
        "full_name": user.full_name,
        "username": user.username,
        "email": user.email,
        "phone": user.phone,
        "role": user.role.value
    }), 200


# Trekker - Browse Open Treks (with filters)
@trekker_bp.route("/treks", methods=["GET"])
@jwt_required()
def browse_treks():
    user_id = int(get_jwt_identity())
    user, trekker = get_logged_in_trekker(user_id)

    if user is None or trekker is None:
        return jsonify({"message": "Access Denied. Trekkers only."}), 403

    query = Trek.query.filter(
        Trek.status == TrekStatus.OPEN,
        Trek.available_slots > 0
    )

    difficulty = request.args.get("difficulty")
    if difficulty:
        try:
            query = query.filter(Trek.difficulty == TrekDifficulty[difficulty.upper()])
        except KeyError:
            pass

    location = request.args.get("location")
    if location:
        query = query.filter(Trek.location.ilike(f"%{location}%"))

    max_duration = request.args.get("max_duration")
    if max_duration:
        try:
            query = query.filter(Trek.duration_days <= int(max_duration))
        except ValueError:
            pass

    treks = query.order_by(Trek.start_date.asc()).all()

    treks_data = []
    for trek in treks:
        treks_data.append({
            "trek_id": trek.trek_id,
            "trek_uuid": trek.trek_uuid,
            "trek_name": trek.trek_name,
            "location": trek.location,
            "difficulty": trek.difficulty.value,
            "duration_days": trek.duration_days,
            "available_slots": trek.available_slots,
            "price": float(trek.price),
            "start_date": trek.start_date.isoformat(),
            "end_date": trek.end_date.isoformat(),
            "status": trek.status.value
        })

    return jsonify({
        "treks": treks_data,
        "total": len(treks_data)
    }), 200


# Trekker - Get One Trek (for booking page)
@trekker_bp.route("/treks/<trek_uuid>", methods=["GET"])
@jwt_required()
def get_trek_for_booking(trek_uuid):
    user_id = int(get_jwt_identity())
    user, trekker = get_logged_in_trekker(user_id)

    if user is None or trekker is None:
        return jsonify({"message": "Access Denied. Trekkers only."}), 403

    trek = Trek.query.filter_by(trek_uuid=trek_uuid).first()

    if not trek:
        return jsonify({"message": "Trek not found."}), 404

    # Check whether this trekker already has an active booking for this trek
    existing_booking = Booking.query.filter(
        Booking.trekker_id == trekker.trekker_id,
        Booking.trek_id == trek.trek_id,
        Booking.booking_status.in_([BookingStatus.PENDING, BookingStatus.APPROVED])
    ).first()

    return jsonify({
        "trek": {
            "trek_id": trek.trek_id,
            "trek_uuid": trek.trek_uuid,
            "trek_name": trek.trek_name,
            "location": trek.location,
            "difficulty": trek.difficulty.value,
            "duration_days": trek.duration_days,
            "capacity": trek.capacity,
            "available_slots": trek.available_slots,
            "price": float(trek.price),
            "start_date": trek.start_date.isoformat(),
            "end_date": trek.end_date.isoformat(),
            "meeting_point": trek.meeting_point,
            "description": trek.description,
            "status": trek.status.value
        },
        "already_booked": existing_booking is not None
    }), 200


# Trekker - Create Booking
@trekker_bp.route("/bookings", methods=["POST"])
@jwt_required()
def create_booking():
    user_id = int(get_jwt_identity())
    user, trekker = get_logged_in_trekker(user_id)

    if user is None or trekker is None:
        return jsonify({"message": "Access Denied. Trekkers only."}), 403

    data = request.get_json() or {}
    trek_uuid = data.get("trek_uuid")
    number_of_people = data.get("number_of_people", 1)

    if not trek_uuid:
        return jsonify({"message": "trek_uuid is required."}), 400

    try:
        number_of_people = int(number_of_people)
        if number_of_people <= 0:
            return jsonify({"message": "Number of people must be at least 1."}), 400
    except (ValueError, TypeError):
        return jsonify({"message": "Number of people must be a valid number."}), 400

    trek = Trek.query.filter_by(trek_uuid=trek_uuid).first()

    if not trek:
        return jsonify({"message": "Trek not found."}), 404

    # Trek must be Open
    if trek.status != TrekStatus.OPEN:
        return jsonify({
            "message": f"This Trek is {trek.status.value} and is not open for booking."
        }), 400

    # Enough slots available
    if trek.available_slots < number_of_people:
        return jsonify({
            "message": f"Only {trek.available_slots} slot(s) available for this Trek."
        }), 400

    # Prevent duplicate active booking by same trekker for same trek
    existing_booking = Booking.query.filter(
        Booking.trekker_id == trekker.trekker_id,
        Booking.trek_id == trek.trek_id,
        Booking.booking_status.in_([BookingStatus.PENDING, BookingStatus.APPROVED])
    ).first()

    if existing_booking:
        return jsonify({
            "message": "You already have an active booking for this Trek."
        }), 409

    try:
        booking_amount = float(trek.price) * number_of_people

        new_booking = Booking(
            trekker_id=trekker.trekker_id,
            trek_id=trek.trek_id,
            number_of_people=number_of_people,
            booking_amount=booking_amount,
            booking_status=BookingStatus.APPROVED,
            payment_status=PaymentStatus.PENDING
        )

        db.session.add(new_booking)

        # Decrement available slots
        trek.available_slots -= number_of_people

        # If slots hit zero, mark trek as Full
        if trek.available_slots == 0:
            trek.status = TrekStatus.FULL

        db.session.commit()

    except Exception as e:
        db.session.rollback()
        print("CREATE BOOKING ERROR:", repr(e))
        return jsonify({
            "message": "Unable to create booking.",
            "error": str(e)
        }), 500

    return jsonify({
        "message": "Trek booked successfully.",
        "booking": {
            "booking_uuid": new_booking.booking_uuid,
            "trek_name": trek.trek_name,
            "number_of_people": new_booking.number_of_people,
            "booking_amount": float(new_booking.booking_amount),
            "booking_status": new_booking.booking_status.value,
            "payment_status": new_booking.payment_status.value,
            "booking_date": new_booking.booking_date.isoformat()
        }
    }), 201


# Trekker - Get My Bookings
@trekker_bp.route("/bookings", methods=["GET"])
@jwt_required()
def get_my_bookings():
    user_id = int(get_jwt_identity())
    user, trekker = get_logged_in_trekker(user_id)

    if user is None or trekker is None:
        return jsonify({"message": "Access Denied. Trekkers only."}), 403

    bookings = Booking.query.filter_by(
        trekker_id=trekker.trekker_id
    ).order_by(Booking.booking_date.desc()).all()

    bookings_data = []
    for booking in bookings:
        bookings_data.append({
            "booking_uuid": booking.booking_uuid,
            "trek_uuid": booking.trek.trek_uuid,
            "trek_name": booking.trek.trek_name,
            "location": booking.trek.location,
            "start_date": booking.trek.start_date.isoformat(),
            "end_date": booking.trek.end_date.isoformat(),
            "number_of_people": booking.number_of_people,
            "booking_amount": float(booking.booking_amount),
            "booking_status": booking.booking_status.value,
            "payment_status": booking.payment_status.value,
            "booking_date": booking.booking_date.isoformat(),
            "trek_status": booking.trek.status.value
        })

    return jsonify({
        "bookings": bookings_data,
        "total": len(bookings_data)
    }), 200


# Trekker - Cancel Booking
@trekker_bp.route("/bookings/<booking_uuid>/cancel", methods=["PATCH"])
@jwt_required()
def cancel_booking(booking_uuid):
    user_id = int(get_jwt_identity())
    user, trekker = get_logged_in_trekker(user_id)

    if user is None or trekker is None:
        return jsonify({"message": "Access Denied. Trekkers only."}), 403

    booking = Booking.query.filter_by(booking_uuid=booking_uuid).first()

    if not booking:
        return jsonify({"message": "Booking not found."}), 404

    if booking.trekker_id != trekker.trekker_id:
        return jsonify({"message": "Access denied. This booking is not yours."}), 403

    if booking.booking_status not in [BookingStatus.PENDING, BookingStatus.APPROVED]:
        return jsonify({
            "message": f"This booking is already {booking.booking_status.value} and cannot be cancelled."
        }), 400

    try:
        booking.booking_status = BookingStatus.CANCELLED

        trek = booking.trek
        trek.available_slots += booking.number_of_people

        # Reopen trek if it was Full and now has space
        if trek.status == TrekStatus.FULL and trek.available_slots > 0:
            trek.status = TrekStatus.OPEN

        db.session.commit()

    except Exception as e:
        db.session.rollback()
        print("CANCEL BOOKING ERROR:", repr(e))
        return jsonify({"message": "Unable to cancel booking."}), 500

    return jsonify({
        "message": "Booking cancelled successfully.",
        "booking": {
            "booking_uuid": booking.booking_uuid,
            "booking_status": booking.booking_status.value
        }
    }), 200
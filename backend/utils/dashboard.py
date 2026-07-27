from sqlalchemy import func

from models import (
    db,
    Staff,
    Trekker,
    Trek,
    Booking,
    TrekStatus
)

def get_dashboard_statistics():

    total_staff = Staff.query.count()
    total_trekkers = Trekker.query.count()
    total_treks = Trek.query.count()
    total_bookings = Booking.query.count()
    total_revenue = (
        db.session.query(
            func.sum(Booking.booking_amount)
        ).scalar() or 0
    )

    upcoming_treks = Trek.query.filter(
        Trek.status == TrekStatus.UPCOMING
    ).count()

    return {
        "totalStaff": total_staff,
        "totalTrekkers": total_trekkers,
        "totalTreks": total_treks,
        "totalBookings": total_bookings,
        "totalRevenue": float(total_revenue),
        "upcomingTreks": upcoming_treks
    }
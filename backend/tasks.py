import csv
import io
from datetime import date, timedelta

from sqlalchemy import func
from flask_mail import Message

from celery_app import celery
from app import app as flask_app
from extensions import db, mail
from models import (
    Trek,
    TrekStatus,
    Booking,
    BookingStatus,
    Trekker,
    User,
    UserRole
)


# Daily Reminder — treks starting tomorrow
@celery.task(name="tasks.send_trek_reminders")
def send_trek_reminders():
    with flask_app.app_context():
        tomorrow = date.today() + timedelta(days=1)

        upcoming_treks = Trek.query.filter(
            Trek.start_date == tomorrow,
            Trek.status == TrekStatus.OPEN
        ).all()

        sent_count = 0

        for trek in upcoming_treks:
            for booking in trek.bookings:
                if booking.booking_status == BookingStatus.APPROVED:
                    try:
                        message = Message(
                            subject=f"Reminder: {trek.trek_name} starts tomorrow!",
                            recipients=[booking.trekker.user.email],
                            body=(
                                f"Hello {booking.trekker.user.full_name},\n\n"
                                f"This is a reminder that your trek '{trek.trek_name}' "
                                f"starts tomorrow ({trek.start_date}).\n\n"
                                f"Meeting Point: {trek.meeting_point or 'To be announced'}\n\n"
                                f"Regards,\nTrekMate"
                            )
                        )
                        mail.send(message)
                        sent_count += 1
                    except Exception as e:
                        print("Reminder Email Error:", e)

        return f"Sent {sent_count} reminder email(s)."

# Monthly Report — sent to Admin
@celery.task(name="tasks.generate_monthly_report")
def generate_monthly_report():
    with flask_app.app_context():
        total_treks = Trek.query.count()

        total_participants = (
            db.session.query(func.sum(Booking.number_of_people)).scalar() or 0
        )

        popular_treks = (
            db.session.query(
                Trek.trek_name,
                func.count(Booking.booking_id).label("booking_count")
            )
            .join(Booking)
            .group_by(Trek.trek_id)
            .order_by(func.count(Booking.booking_id).desc())
            .limit(5)
            .all()
        )

        report_html = f"""
        <h2>Monthly Trekking Report</h2>
        <p><strong>Total Treks:</strong> {total_treks}</p>
        <p><strong>Total Participants:</strong> {total_participants}</p>
        <h3>Most Popular Treks</h3>
        <ul>
        """
        for trek_name, booking_count in popular_treks:
            report_html += f"<li>{trek_name} — {booking_count} bookings</li>"
        report_html += "</ul>"

        admin = User.query.filter_by(role=UserRole.ADMIN).first()

        if admin:
            try:
                message = Message(
                    subject="Monthly Trekking Activity Report",
                    recipients=[admin.email],
                    html=report_html
                )
                mail.send(message)
            except Exception as e:
                print("Monthly Report Email Error:", e)

        return "Monthly report generated and sent."


# User-Triggered CSV Export
@celery.task(name="tasks.export_trekking_history_csv")
def export_trekking_history_csv(trekker_id):
    with flask_app.app_context():
        trekker = db.session.get(Trekker, trekker_id)

        if not trekker:
            return "Trekker not found."

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow([
            "Trek Name", "Location", "Start Date", "End Date",
            "People", "Amount", "Booking Status", "Payment Status"
        ])

        for booking in trekker.bookings:
            writer.writerow([
                booking.trek.trek_name,
                booking.trek.location,
                booking.trek.start_date,
                booking.trek.end_date,
                booking.number_of_people,
                booking.booking_amount,
                booking.booking_status.value,
                booking.payment_status.value
            ])

        csv_content = output.getvalue()

        try:
            message = Message(
                subject="Your Trekking History Export",
                recipients=[trekker.user.email],
                body="Please find attached your trekking history CSV export."
            )
            message.attach("trekking_history.csv", "text/csv", csv_content)
            mail.send(message)
        except Exception as e:
            print("CSV Export Email Error:", e)
            return f"Failed: {e}"

        return "CSV export emailed successfully."
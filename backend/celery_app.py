from celery import Celery
from celery.schedules import crontab

celery = Celery(
    "trekking_management",
    broker="redis://localhost:6379/1",
    backend="redis://localhost:6379/1"
)

celery.conf.timezone = "Asia/Kolkata"

celery.conf.beat_schedule = {
    "daily-trek-reminders": {
        "task": "tasks.send_trek_reminders",
        "schedule": crontab(hour=8, minute=0),
    },
    "monthly-trekking-report": {
        "task": "tasks.generate_monthly_report",
        "schedule": crontab(day_of_month=1, hour=6, minute=0),
    },
}
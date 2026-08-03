from celery_worker import celery_app

from flask import render_template

from models import User, Trek, Booking

from mail_service import send_email


@celery_app.task
def send_daily_reminder():

    users = User.query.filter_by(role="user").all()

    for user in users:

        html = render_template(
            "daily_reminder.html",
            name=user.name
        )

        send_email(
            user.email,
            "Daily Trek Reminder",
            html
        )

    return "Daily Reminder Sent"


@celery_app.task
def send_monthly_report():

    admin = User.query.filter_by(role="admin").first()

    if not admin:

        return "Admin Not Found"

    html = render_template(

        "monthly_report.html",

        total_bookings=Booking.query.count(),

        total_treks=Trek.query.count()

    )

    send_email(

        admin.email,

        "Monthly Trek Report",

        html

    )

    return "Monthly Report Sent"
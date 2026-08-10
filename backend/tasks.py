from celery_worker import celery_app

from flask import render_template

from models import db, User, Trek, Booking

from mail_service import send_email
import csv
import os
from datetime import datetime
@celery_app.task
def send_daily_reminder():

    users = User.query.filter_by(role="user").all()

    for user in users:

        bookings = Booking.query.filter_by(
            user_id=user.id,
            status="Approved"
        ).all()

        treks = []

        for booking in bookings:

            trek = Trek.query.get(booking.trek_id)

            if trek and trek.start_date >= datetime.today().date():

                treks.append(trek)

        if treks:

            html = render_template(
                "daily_reminder.html",
                name=user.name,
                treks=treks
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

    total_treks = Trek.query.count()

    total_users = User.query.filter_by(role="user").count()

    total_participants = Booking.query.filter_by(
        status="Approved"
    ).count()

    popular_trek = (
        Trek.query
        .join(Booking, Trek.id == Booking.trek_id)
        .group_by(Trek.id)
        .order_by(db.func.count(Booking.id).desc())
        .first()
    )

    html = render_template(
        "monthly_report.html",
        total_treks=total_treks,
        total_users=total_users,
        total_participants=total_participants,
        popular_trek=popular_trek
    )

    send_email(
        admin.email,
        "Monthly Trek Report",
        html
    )

    return "Monthly Report Sent"


@celery_app.task
def export_booking_history(user_id):

    user = User.query.get(user_id)

    if not user:
        return "User Not Found"

    bookings = Booking.query.filter_by(
        user_id=user.id
    ).all()

    filename = f"booking_history_{user.id}.csv"

    with open(filename, "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            "User ID",
            "Trek Name",
            "Location",
            "Booking Status",
            "Booking Date"
        ])

        for booking in bookings:

            trek = Trek.query.get(booking.trek_id)

            if not trek:
                continue

            writer.writerow([
                user.id,
                trek.name,
                trek.location,
                booking.status,
                booking.booking_date
            ])

    send_email(
        user.email,
        "Booking History Export",
        f"Your booking history has been exported successfully.\n\nFile Name: {filename}"
    )

    return filename
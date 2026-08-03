import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


SMTP_HOST = "localhost"
SMTP_PORT = 1025

SENDER_EMAIL = "admin@trek.com"


def send_email(to_email, subject, body):

    message = MIMEMultipart()

    message["From"] = SENDER_EMAIL
    message["To"] = to_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP(
        SMTP_HOST,
        SMTP_PORT
    )

    server.send_message(message)

    server.quit()
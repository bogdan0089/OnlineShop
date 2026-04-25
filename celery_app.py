import smtplib
from email.mime.text import MIMEText
from celery import Celery
from core.config import settings
from core.enum import OrderStatus


celery = Celery(
    "tasks",
    broker=f"{settings.REDIS_URL}/0",
    backend=f"{settings.REDIS_URL}/0",
)


@celery.task
def send_verification_email(to_email: str, token: str):
    message = MIMEText(f"Click to verify your email:\n{settings.FRONTEND_URL}/auth/verify/{token}")
    message["Subject"] = "Verification email"
    message["From"] = settings.EMAIL_USER
    message["To"] = to_email
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(settings.EMAIL_USER, settings.EMAIL_PASSWORD)
        server.sendmail(settings.EMAIL_USER, to_email, message.as_string())


@celery.task
def send_reset_password_email(to_email: str, token: str):
    message = MIMEText(f"Click to reset your password:\n{settings.FRONTEND_URL}/reset-password?token={token}")
    message["Subject"] = "Password reset"
    message["From"] = settings.EMAIL_USER
    message["To"] = to_email
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(settings.EMAIL_USER, settings.EMAIL_PASSWORD)
        server.sendmail(settings.EMAIL_USER, to_email, message.as_string())


@celery.task
def send_order_status_email(to_email: str, order_id: int, status: OrderStatus):
    message = MIMEText(f"Your order {order_id} status changed to {status}")
    message["Subject"] = "Order update"
    message["From"] = settings.EMAIL_USER
    message["To"] = to_email
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(settings.EMAIL_USER, settings.EMAIL_PASSWORD)
        server.sendmail(settings.EMAIL_USER, to_email, message.as_string())

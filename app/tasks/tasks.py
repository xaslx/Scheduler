import smtplib
from time import sleep

from pydantic import EmailStr

from app.tasks.celery_app import celery
from app.tasks.email_templates import (add_new_client, cancel_booking,
                                       confirm_booking,
                                       forgot_password_email_template,
                                       get_help,
                                       password_changed_email_template,
                                       register_confirmation_template,
                                       send_notification_for_all_users,
                                       success_update_password)
from config import settings


@celery.task
def register_confirmation_message(email_to: EmailStr):
    msg_content = register_confirmation_template(email_to=email_to)

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg_content)


@celery.task
def reset_password_email(email: EmailStr, token: str):
    msg_content = forgot_password_email_template(email, token)

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg_content)


@celery.task
def password_changed(email: EmailStr, new_password: str):

    msg_content = password_changed_email_template(email, new_password)

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg_content)


@celery.task
def update_password(email: EmailStr, new_password: str):

    msg_content = success_update_password(email_to=email, new_password=new_password)

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg_content)


@celery.task
def new_client(email: EmailStr, date: str, time: str, name: str, phone_number: str, user_email: EmailStr, tg: str):
    msg_content = add_new_client(email_to=email, date=date, time=time, name=name, phone_number=phone_number, user_email=user_email, tg=tg)

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg_content)


@celery.task
def cancel_client(
    message: str, email: EmailStr, date: str, time: str, description: str
):
    msg_content = cancel_booking(
        message=message, email_to=email, date=date, time=time, description=description
    )

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg_content)


@celery.task
def send_notification(users: list, message: str):

    for user in users:
        msg_content = send_notification_for_all_users(user, message)

        sleep(1)
        with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.login(settings.SMTP_USER, settings.SMTP_PASS)
            server.send_message(msg_content)


@celery.task
def help_message(email: EmailStr, description: str):
    msg_content = get_help(email_from=email, description=description)

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg_content)


@celery.task
def confirm_booking_for_client(
    email_to: EmailStr, tg: str, em: EmailStr, time: str, date: str
):
    msg_content = confirm_booking(email_to=email_to, tg=tg, em=em, time=time, date=date)

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg_content)

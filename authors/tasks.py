from celery import shared_task

from utils.functions import welcome_email


@shared_task(name="send_welcome_email")
def task_welcome_email(username: str, email: str):
    welcome_email(username, email)

    return email

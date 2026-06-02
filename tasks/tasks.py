from utils.functions import welcome_email


# @shared_task
def task_welcome_email(username: str, email: str):
    welcome_email(username, email)

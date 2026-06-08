from datetime import datetime

from celery import shared_task
from decouple import config
from django.core.mail import send_mail

from .models import Task


@shared_task(name="deadline_billing")
def task_deadline_billing() -> None:
    overdue_tasks = Task.objects.filter(
        deadline__isnull=False,
        deadline__lt=datetime.now().date(),
        completed=False,
    )

    for task in overdue_tasks:
        html_message = f'''
<p>Olá <strong>{task.author.username.upper()}</strong>, você tem uma tarefa atrasada:<br> <strong>{task.title.upper()}</strong>.</p>
<p>Por favor, acesse o sistema para verificar os detalhes e tomar as medidas necessárias.</p>
<p>Acesse o sistema: <a href="{config("DOMAIN_NAME", default="http://127.0.0.1:8000")}/tasks/?completed=overdue">clique aqui</a></p>
<p>Atenciosamente,<br>Equipe <strong>Fokus Manager</strong></p>
        '''
        send_mail(
            subject="LEMBRE-SE DAS SUAS TAREFAS",
            message="",
            from_email=config("EMAIL_HOST_USER"),
            recipient_list=[task.author.email],
            html_message=html_message,
        )

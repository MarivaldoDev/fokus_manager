import logging
from functools import wraps

from django.shortcuts import get_object_or_404, redirect

from tasks.models import Task

logger = logging.getLogger(__name__)


def user_only(view_func):
    """
    Permite o usuário acessar apenas suas próprias informações.
    Evita que usuários acessem dados de outros usuários.
    """

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        task_id = kwargs.get("task_id") or kwargs.get("pk")

        if task_id:
            task = get_object_or_404(Task, pk=task_id)
            if task.author != request.user:
                return redirect("tasks:home")

        return view_func(request, *args, **kwargs)

    return wrapper

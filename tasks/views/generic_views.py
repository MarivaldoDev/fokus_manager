import logging

from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import render

from tasks.decorators.decorator import user_only
from tasks.models import Category, Task
from utils.functions import _build_productivity_chart

logger = logging.getLogger(__name__)


def home(request):
    logger.info("Acessando a página inicial.")
    return render(request, "home.html")


@login_required(login_url="authors:login")
@user_only
def dashboard(request):
    user_tasks = Task.objects.filter(author=request.user)
    tasks = user_tasks.aggregate(
        open_count=Count("id", filter=Q(completed=False)),
        completed_count=Count("id", filter=Q(completed=True)),
    )

    categories_with_open_count = (
        Category.objects.filter(author=request.user, tasks__completed=False)
        .distinct()
        .count()
    )

    recents_tasks = user_tasks.order_by("-created_at")[:5]
    completed_tasks = user_tasks.filter(completed=True, finish_date__isnull=False)

    return render(
        request,
        "dashboard.html",
        {
            "open_tasks": tasks["open_count"],
            "completed_tasks": tasks["completed_count"],
            "categories_with_open_count": categories_with_open_count,
            "recents_tasks": recents_tasks,
            "productivity_chart": _build_productivity_chart(completed_tasks),
        },
    )

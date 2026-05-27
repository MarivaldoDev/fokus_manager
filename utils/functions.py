from collections import Counter
from datetime import date, timedelta

from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone


def list_errors(request, form):
    for field, errors in form.errors.items():
        for error in errors:
            messages.error(request, error)


def pagination(request, queryset, per_page=5):
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return page_obj


MONTH_LABELS = (
    "Jan",
    "Fev",
    "Mar",
    "Abr",
    "Mai",
    "Jun",
    "Jul",
    "Ago",
    "Set",
    "Out",
    "Nov",
    "Dez",
)


def _month_start(reference_date: date, months_back: int) -> date:
    month = reference_date.month - months_back
    year = reference_date.year

    while month <= 0:
        month += 12
        year -= 1

    return date(year, month, 1)


def _build_productivity_chart(task_queryset):
    today = timezone.localdate()
    current_week_start = today - timedelta(days=today.weekday())
    weekly_periods = [
        current_week_start - timedelta(weeks=offset) for offset in range(7, -1, -1)
    ]
    monthly_periods = [_month_start(today, offset) for offset in range(5, -1, -1)]

    completed_dates = task_queryset.values_list("finish_date", flat=True)

    weekly_counter = Counter(
        finish_date - timedelta(days=finish_date.weekday())
        for finish_date in completed_dates
        if finish_date and finish_date >= weekly_periods[0]
    )
    monthly_counter = Counter(
        finish_date.replace(day=1)
        for finish_date in completed_dates
        if finish_date and finish_date >= monthly_periods[0]
    )

    return {
        "weekly": {
            "labels": [f"{period.strftime('%d/%m')}" for period in weekly_periods],
            "data": [weekly_counter.get(period, 0) for period in weekly_periods],
        },
        "monthly": {
            "labels": [
                f"{MONTH_LABELS[period.month - 1]}/{period.year}"
                for period in monthly_periods
            ],
            "data": [monthly_counter.get(period, 0) for period in monthly_periods],
        },
    }

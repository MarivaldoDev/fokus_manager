import logging
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from utils.functions import list_errors, pagination

from ..decorators.decorator import user_only
from ..forms import TaskFilterForm, TaskForm, TaskUpdateForm
from ..models import Category, Task

logger = logging.getLogger(__name__)


@method_decorator(login_required(login_url="authors:login"), name="dispatch")
class CreateTask(CreateView):
    model = Task
    form_class = TaskForm
    template_name = "create_task.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Tarefa criada com sucesso!")
        return super().form_valid(form)

    def form_invalid(self, form):
        list_errors(self.request, form)
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse("tasks:tasks")


@method_decorator(
    [login_required(login_url="authors:login"), user_only], name="dispatch"
)
class UpdateTask(UpdateView):
    model = Task
    form_class = TaskUpdateForm
    template_name = "update_task.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_object(self, queryset=None):
        slug = self.kwargs.get(self.slug_url_kwarg)
        return get_object_or_404(Task, slug=slug, author=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_invalid(self, form):
        list_errors(self.request, form)
        return super().form_invalid(form)

    def form_valid(self, form):
        if not form.has_changed():
            return redirect(self.get_success_url())
        messages.success(self.request, "Tarefa atualizada com sucesso!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("tasks:task_detail", kwargs={"slug": self.object.slug})


@method_decorator(
    [login_required(login_url="authors:login"), user_only], name="dispatch"
)
class DeleteTask(DeleteView):
    model = Task
    template_name = "task_detail.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_object(self, queryset=None):
        slug = self.kwargs.get(self.slug_url_kwarg)
        return get_object_or_404(Task, slug=slug, author=self.request.user)

    def get_success_url(self):
        messages.success(self.request, "Tarefa excluída com sucesso!")
        return reverse("tasks:tasks")


@login_required(login_url="authors:login")
@user_only
def toggle_task_completed(request, slug: str):
    task = get_object_or_404(Task, slug=slug, author=request.user)

    if request.method == "POST":
        task.completed = "completed" in request.POST
        task.finish_date = datetime.now().date() if task.completed else None
        task.save()

    return redirect("tasks:task_detail", slug=task.slug)


@login_required(login_url="authors:login")
@user_only
def tasks_by_category(request, slug: str):
    category = get_object_or_404(Category, author=request.user, slug=slug)
    tasks = Task.objects.filter(author=request.user, category=category)

    filter_form = TaskFilterForm(request.GET or None, user=request.user)
    if filter_form.is_valid():
        cd = filter_form.cleaned_data
        if cd.get("title"):
            tasks = tasks.filter(title__icontains=cd["title"])
        if cd.get("start_date_from"):
            tasks = tasks.filter(start_date__gte=cd["start_date_from"])
        if cd.get("start_date_to"):
            tasks = tasks.filter(start_date__lte=cd["start_date_to"])
        if cd.get("completed") == "yes":
            tasks = tasks.filter(completed=True)
        elif cd.get("completed") == "no":
            tasks = tasks.filter(completed=False)

    page_obj = pagination(request, tasks, per_page=6)

    return render(
        request,
        "tasks.html",
        {"page_obj": page_obj, "category": category, "filter_form": filter_form},
    )


@login_required(login_url="authors:login")
@user_only
def task_list(request):
    tasks = Task.objects.filter(author=request.user).order_by("start_date")

    filter_form = TaskFilterForm(request.GET or None, user=request.user)
    if filter_form.is_valid():
        cd = filter_form.cleaned_data
        if cd.get("category"):
            tasks = tasks.filter(category=cd["category"])
        if cd.get("title"):
            tasks = tasks.filter(title__icontains=cd["title"])
        if cd.get("start_date_from"):
            tasks = tasks.filter(start_date__gte=cd["start_date_from"])
        if cd.get("start_date_to"):
            tasks = tasks.filter(start_date__lte=cd["start_date_to"])
        if cd.get("completed") == "yes":
            tasks = tasks.filter(completed=True)
        elif cd.get("completed") == "no":
            tasks = tasks.filter(completed=False)

    page_obj = pagination(request, tasks, per_page=6)
    categories = Category.objects.filter(author=request.user)

    return render(
        request,
        "tasks.html",
        {"page_obj": page_obj, "filter_form": filter_form, "categories": categories},
    )


@login_required(login_url="authors:login")
@user_only
def task_detail(request, slug: str):
    task = get_object_or_404(Task, author=request.user, slug=slug)
    return render(request, "task_detail.html", {"task": task})

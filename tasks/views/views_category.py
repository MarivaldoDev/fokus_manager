import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from utils.functions import list_errors

from ..decorators.decorator import user_only
from ..forms import CategoryForm, CategoryUpdateForm
from ..models import Category

logger = logging.getLogger(__name__)


@method_decorator(login_required(login_url="authors:login"), name="dispatch")
class CreateCategory(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "create_category.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Categoria criada com sucesso!")
        return super().form_valid(form)

    def form_invalid(self, form):
        list_errors(self.request, form)
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse("tasks:dashboard")


@method_decorator(
    [login_required(login_url="authors:login"), user_only], name="dispatch"
)
class UpdateCategory(UpdateView):
    model = Category
    form_class = CategoryUpdateForm
    template_name = "update_category.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_object(self, queryset=None):
        slug = self.kwargs.get(self.slug_url_kwarg)
        return get_object_or_404(Category, slug=slug, author=self.request.user)

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
        messages.success(self.request, "Categoria atualizada com sucesso!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("tasks:dashboard")


@method_decorator(
    [login_required(login_url="authors:login"), user_only], name="dispatch"
)
class DeleteCategory(DeleteView):
    model = Category
    template_name = "categories.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_object(self, queryset=None):
        slug = self.kwargs.get(self.slug_url_kwarg)
        return get_object_or_404(Category, slug=slug, author=self.request.user)

    def get_success_url(self):
        messages.success(self.request, "Categoria excluída com sucesso!")
        return reverse("tasks:dashboard")


@login_required(login_url="authors:login")
@user_only
def category_list(request):
    all_categories = Category.objects.filter(author=request.user)

    categories_with_tasks_incomplete = Category.objects.annotate(
        incomplete_count=Count(
            "tasks", filter=Q(tasks__author=request.user.id, tasks__completed=False)
        )
    ).filter(incomplete_count__gt=0)

    # Determina qual filtro aplicar
    filter_type = request.GET.get("filter", "incomplete")
    if filter_type == "all":
        categories_to_display = all_categories
    else:
        categories_to_display = categories_with_tasks_incomplete

    return render(
        request,
        "categories.html",
        {
            "all_categories": all_categories,
            "categories_with_tasks_incomplete": categories_with_tasks_incomplete,
            "categories_to_display": categories_to_display,
            "filter_type": filter_type,
        },
    )

import logging
from typing import cast

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.db.models import QuerySet
from django.forms import BaseModelForm
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from utils.functions import list_errors

from .forms import RegisterForm, UpdateRegisterForm
from .models import Author
from .tasks import task_welcome_email

logger = logging.getLogger(__name__)


class RegisterView(CreateView):
    model = Author
    template_name = "authors/pages/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("authors:login")

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        list_errors(self.request, form)
        return super().form_invalid(form)

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.save()
        messages.success(
            self.request,
            "Seu cadastro foi realizado com sucesso! Faça login para acessar o dashboard.",
        )

        task_welcome_email.delay(  # type: ignore
            username=form.cleaned_data["username"], email=form.cleaned_data["email"]
        )
        return super().form_valid(form)


class RegisterUpdateView(UpdateView):
    model = Author
    template_name = "authors/pages/update.html"
    form_class = UpdateRegisterForm
    success_url = reverse_lazy("tasks:dashboard")

    def get_object(self, queryset: QuerySet | None = None) -> Author:
        return cast(Author, self.request.user)

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.save()
        messages.success(self.request, "Seu perfil foi atualizado com sucesso!")
        return super().form_valid(form)

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        list_errors(self.request, form)
        return super().form_invalid(form)


class RegisterDeleteView(DeleteView):
    model = Author
    template_name = "dashboard.html"
    success_url = reverse_lazy("tasks:home")

    def get_object(self, queryset: QuerySet | None = None) -> Author:
        return cast(Author, self.request.user)

    def delete(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        messages.success(
            self.request, "Seu perfil foi deletado com sucesso! Sentiremos sua falta."
        )
        return super().delete(request, *args, **kwargs)


class MyLoginView(LoginView):
    template_name = "authors/pages/login.html"

    def form_invalid(self, form: AuthenticationForm) -> HttpResponse:
        list_errors(self.request, form)
        return super().form_invalid(form)

    def get_success_url(self) -> str:
        return reverse("tasks:dashboard")


@login_required(login_url="authors:login")
def logout_view(request: HttpRequest) -> HttpResponseRedirect:
    logout(request)
    return redirect("tasks:home")

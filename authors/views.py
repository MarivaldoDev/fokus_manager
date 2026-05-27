import logging

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from utils.functions import list_errors

from .forms import RegisterForm, UpdateRegisterForm
from .models import Author

logger = logging.getLogger(__name__)


class RegisterView(CreateView):
    model = Author
    template_name = "authors/pages/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("authors:login")

    def form_invalid(self, form):
        list_errors(self.request, form)
        return super().form_invalid(form)

    def form_valid(self, form):
        form.save()
        messages.success(
            self.request,
            "Seu cadastro foi realizado com sucesso! Faça login para acessar o dashboard.",
        )
        return super().form_valid(form)


class RegisterUpdateView(UpdateView):
    model = Author
    template_name = "authors/pages/update.html"
    form_class = UpdateRegisterForm
    success_url = reverse_lazy("tasks:dashboard")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Seu perfil foi atualizado com sucesso!")
        return super().form_valid(form)

    def form_invalid(self, form):
        list_errors(self.request, form)
        return super().form_invalid(form)


class RegisterDeleteView(DeleteView):
    model = Author
    template_name = "dashboard.html"
    success_url = reverse_lazy("tasks:home")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(
            self.request, "Seu perfil foi deletado com sucesso! Sentiremos sua falta."
        )
        return super().form_valid(form)


class MyLoginView(LoginView):
    template_name = "authors/pages/login.html"

    def form_invalid(self, form):
        list_errors(self.request, form)
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse("tasks:dashboard")


@login_required(login_url="authors:login")
def logout_view(request):
    logout(request)
    return redirect("tasks:home")

from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from . import views

app_name = "authors"

urlpatterns = [
    path("register/create/", views.RegisterView.as_view(), name="register"),
    path("register/update/", views.RegisterUpdateView.as_view(), name="update"),
    path("register/delete/", views.RegisterDeleteView.as_view(), name="delete"),
    path("login/", views.MyLoginView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="authors/registration/password_reset_form.html",
            email_template_name="authors/registration/password_reset_email.html",
            success_url=reverse_lazy("authors:password_reset_done"),
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="authors/registration/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "password_reset_confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="authors/registration/password_reset_confirm.html",
            success_url=reverse_lazy("authors:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "password_reset_complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="authors/registration/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]

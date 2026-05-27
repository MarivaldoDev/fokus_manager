from django.contrib.auth import views as auth_views
from django.urls import resolve, reverse

from .test_base_authors import AuthorsTestBase


class AuthorsViewsTests(AuthorsTestBase):
    def test_authors_register_view_returns_error_message_on_invalid_form(self):
        response = self.client.post(reverse("authors:register"), data={})
        content = response.content.decode("utf-8")

        self.assertIn("Todos os campos são obrigatórios.", content)

    def test_authors_register_view_loads_blank_form_if_request_is_get(self):
        response = self.client.get(reverse("authors:register"))
        form = response.context["form"]

        self.assertFalse(form.is_bound)

    def test_authors_login_view_returns_error_message_on_invalid_form(self):
        response = self.client.post(reverse("authors:login"), data={})
        content = response.content.decode("utf-8")

        self.assertIn("Este campo é obrigatório.", content)

    def test_authors_logout_view_logs_out_user_and_redirects_to_home(self):
        user = self.make_user("test")
        self.client.force_login(user)
        response = self.client.get(reverse("authors:logout"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("tasks:home"))

    def test_authors_update_view_redirects_to_dashboard_on_successful_update(self):
        user = self.make_user(username="test")
        self.client.force_login(user)
        response = self.client.post(
            reverse("authors:update"),
            data={"username": "updated_user", "email": "updated_user@example.com"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("tasks:dashboard"))

    def test_authors_reset_password_view_view_function_is_correct(self):
        view = resolve(reverse("authors:password_reset"))
        self.assertIs(view.func.view_class, auth_views.PasswordResetView)

    def test_authors_reset_password_view_redirects_to_password_reset_done_on_successful_submission(
        self,
    ):
        user = self.make_user(username="test", email="test@example.com")
        response = self.client.post(
            reverse("authors:password_reset"),
            data={"email": user.email},
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("authors:password_reset_done"))

    def test_authors_reset_done_view_loads_message_on_get(self):
        response = self.client.get(reverse("authors:password_reset_done"))
        content = response.content.decode("utf-8")

        self.assertIn("Redefinição de senha enviada", content)
        self.assertTemplateUsed(
            response, "authors/registration/password_reset_done.html"
        )

    def test_authors_reset_done_view_view_function_is_correct(self):
        view = resolve(reverse("authors:password_reset_done"))
        self.assertIs(view.func.view_class, auth_views.PasswordResetDoneView)

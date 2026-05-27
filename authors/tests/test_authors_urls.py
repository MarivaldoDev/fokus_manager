from django.test import TestCase
from django.urls import reverse


class AuthorsURLsTests(TestCase):
    def test_authors_register_url_is_correct(self):
        url = reverse("authors:register")
        self.assertEqual(url, "/authors/register/create/")

    def test_authors_login_url_is_correct(self):
        url = reverse("authors:login")
        self.assertEqual(url, "/authors/login/")

    def test_authors_logout_url_is_correct(self):
        url = reverse("authors:logout")
        self.assertEqual(url, "/authors/logout/")

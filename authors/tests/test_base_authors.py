from django.test import TestCase

from authors.models import Author


class AuthorsTestBase(TestCase):
    def setUp(self):
        self.user = self.make_user()
        self.client.force_login(self.user)
        return super().setUp()

    def make_user(self, username="user", password="123456Test", **kwargs):
        return Author.objects.create_user(
            username=username, password=password, **kwargs
        )

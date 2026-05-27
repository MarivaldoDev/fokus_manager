from django.test import TestCase
from django.utils import timezone

from authors.models import Author

from ..models import Category, Task


class TasksTestBase(TestCase):
    def setUp(self):
        self.user = self.make_user()
        self.client.force_login(self.user)
        return super().setUp()

    def make_category(self, name="Category", author: str | None = None):
        if author is None:
            author_obj = self.user
        elif isinstance(author, str):
            author_obj, _ = Author.objects.get_or_create(username=author)
        else:
            author_obj = author
        return Category.objects.create(name=name, author=author_obj)

    def make_user(self, username="user", password="123456"):
        return Author.objects.create(username=username, password=password)

    def make_task(
        self,
        title="Task 1",
        description="Description for Task 1",
        category_data=None,
        author_data=None,
        start_date="2026-01-01",
        completed=False,
        finish_date=None,
    ):
        # normaliza author_data
        if isinstance(author_data, str):
            author_obj, _ = Author.objects.get_or_create(username=author_data)
        elif author_data is None:
            author_obj = self.user
        else:
            author_obj = author_data

        # só resolve/ cria category se recebido
        if not category_data:
            category = None
        else:
            if "author" not in category_data:
                category_data["author"] = author_obj
            category, _ = Category.objects.get_or_create(**category_data)

        return Task.objects.create(
            title=title,
            description=description,
            category=category,
            author=author_obj,
            start_date=start_date,
            completed=completed,
            finish_date=finish_date
            if finish_date is not None
            else (timezone.localdate() if completed else None),
        )

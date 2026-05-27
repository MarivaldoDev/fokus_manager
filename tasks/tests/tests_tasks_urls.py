from django.test import TestCase
from django.urls import reverse


class TasksURLsTests(TestCase):
    def test_tasks_home_url_is_correct(self):
        url = reverse("tasks:home")
        self.assertEqual(url, "/")

    def test_tasks_tasks_by_category_url_is_correct(self):
        url = reverse("tasks:tasks_by_category", kwargs={"slug": "work"})
        self.assertEqual(url, "/tasks/category/work/")

    def test_tasks_category_url_is_correct(self):
        url = reverse("tasks:categories")
        self.assertEqual(url, "/categories/")

    def test_tasks_tasks_url_is_correct(self):
        url = reverse("tasks:tasks")
        self.assertEqual(url, "/tasks/")

    def test_tasks_task_detail_url_is_correct(self):
        url = reverse("tasks:task_detail", kwargs={"slug": "work"})
        self.assertEqual(url, "/tasks/details/work/")

    def test_tasks_toggle_task_completed_url_is_correct(self):
        url = reverse("tasks:toggle_task_completed", kwargs={"slug": "work"})
        self.assertEqual(url, "/tasks/details/work/toggle/")

from collections import Counter
from datetime import timedelta

from django.urls import resolve, reverse
from django.utils import timezone

from ..views import generic_views, views_category, views_tasks
from .test_base_tasks import TasksTestBase


class TasksViewsTests(TasksTestBase):
    def test_tasks_home_view_function_is_correct(self):
        view = resolve(reverse("tasks:home"))
        self.assertIs(view.func, generic_views.home)

    def test_tasks_tasks_view_function_is_correct(self):
        view = resolve(reverse("tasks:tasks"))
        self.assertIs(view.func, views_tasks.task_list)

    def test_tasks_category_view_function_is_correct(self):
        view = resolve(reverse("tasks:categories"))
        self.assertIs(view.func, views_category.category_list)

    def test_tasks_category_view_loads_categories_where_tasks_exist(self):
        self.make_category(name="Category 1", author="Tester")
        self.make_category(name="Category 2", author="Tester")
        self.make_task(category_data={"name": "Category 1"})

        response = self.client.get(reverse("tasks:categories"))
        content = response.content.decode("utf-8")
        response_context_categories = response.context[
            "categories_with_tasks_incomplete"
        ]

        self.assertIn("Category 1", content)
        self.assertNotIn("Category 2", content)
        self.assertEqual(len(response_context_categories), 1)

    def test_tasks_tasks_by_category_view_function_is_correct(self):
        view = resolve(reverse("tasks:tasks_by_category", kwargs={"slug": "work"}))
        self.assertIs(view.func, views_tasks.tasks_by_category)

    def test_tasks_tasks_by_category_view_category_not_found_returns_404(self):
        category = self.make_category()
        response = self.client.get(
            reverse(
                "tasks:tasks_by_category", kwargs={"slug": category.slug + "-invalid"}
            )
        )
        self.assertEqual(response.status_code, 404)

    def test_tasks_tasks_by_category_view_loads_tasks(self):
        self.make_task(category_data={"name": "Work"})
        response = self.client.get(
            reverse("tasks:tasks_by_category", kwargs={"slug": "work"})
        )

        content = response.content.decode("utf-8")
        response_context_tasks = response.context["page_obj"]

        self.assertIn("Task 1", content)
        self.assertEqual(len(response_context_tasks), 1)

    def test_tasks_home_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse("tasks:home"))
        self.assertEqual(response.status_code, 200)

    def test_tasks_home_view_loads_correct_template(self):
        response = self.client.get(reverse("tasks:home"))
        self.assertTemplateUsed(response, "home.html")

    def test_tasks_dashboard_view_provides_productivity_chart_data(self):
        today = timezone.localdate()
        previous_week = today - timedelta(weeks=1)
        previous_month = (today.replace(day=1) - timedelta(days=1)).replace(day=15)

        self.make_task(title="Current Week", completed=True, finish_date=today)
        self.make_task(title="Previous Week", completed=True, finish_date=previous_week)
        self.make_task(
            title="Previous Month", completed=True, finish_date=previous_month
        )

        response = self.client.get(reverse("tasks:dashboard"))
        chart = response.context["productivity_chart"]
        current_week_start = today - timedelta(days=today.weekday())
        current_week_start - timedelta(weeks=1)
        current_month_start = today.replace(day=1)
        previous_month_start = (current_month_start - timedelta(days=1)).replace(day=1)
        monthly_counter = Counter(
            task_date.replace(day=1)
            for task_date in [today, previous_week, previous_month]
        )

        self.assertEqual(len(chart["weekly"]["labels"]), 8)
        self.assertEqual(len(chart["monthly"]["labels"]), 6)
        self.assertEqual(chart["weekly"]["data"][-1], 1)
        self.assertEqual(chart["weekly"]["data"][-2], 1)
        self.assertEqual(
            chart["monthly"]["data"][-1], monthly_counter[current_month_start]
        )
        self.assertEqual(
            chart["monthly"]["data"][-2], monthly_counter[previous_month_start]
        )

    def test_tasks_tasks_template_shows_no_tasks_message_when_no_tasks(self):
        response = self.client.get(reverse("tasks:tasks"))
        self.assertIn(b"Nenhuma tarefa para exibir.", response.content)

    def test_tasks_tasks_template_loads_tasks(self):
        self.make_task()
        response = self.client.get(reverse("tasks:tasks"))
        content = response.content.decode("utf-8")
        response_context_tasks = response.context["page_obj"]

        self.assertIn("Task 1", content)
        self.assertEqual(len(response_context_tasks), 1)

    def test_tasks_task_detail_view_function_is_correct(self):
        view = resolve(reverse("tasks:task_detail", kwargs={"slug": "work"}))
        self.assertIs(view.func, views_tasks.task_detail)

    def test_tasks_task_detail_view_task_not_found_returns_404(self):
        task = self.make_task()
        response = self.client.get(
            reverse("tasks:task_detail", kwargs={"slug": task.slug + "-invalid"})
        )
        self.assertEqual(response.status_code, 404)

    def test_tasks_task_detail_view_loads_task(self):
        task = self.make_task()
        response = self.client.get(
            reverse("tasks:task_detail", kwargs={"slug": task.slug})
        )
        content = response.content.decode("utf-8")
        response_context_task = response.context["task"]

        self.assertIn("Task 1", content)
        self.assertEqual(response_context_task, task)

    def test_tasks_toggle_task_completed_view_function_is_correct(self):
        view = resolve(reverse("tasks:toggle_task_completed", kwargs={"slug": "work"}))
        self.assertIs(view.func, views_tasks.toggle_task_completed)

    def test_tasks_toggle_task_completed_view_task_not_found_returns_404(self):
        task = self.make_task()
        response = self.client.get(
            reverse(
                "tasks:toggle_task_completed", kwargs={"slug": task.slug + "-invalid"}
            )
        )
        self.assertEqual(response.status_code, 404)

    def test_tasks_toggle_task_completed_view_marks_task_as_completed(self):
        task = self.make_task()
        response = self.client.post(
            reverse("tasks:toggle_task_completed", kwargs={"slug": task.slug}),
            data={"completed": "completed"},
        )
        task.refresh_from_db()
        self.assertTrue(task.completed)
        self.assertEqual(response.status_code, 302)

    def test_tasks_toggle_task_completed_view_marks_task_as_not_completed(self):
        task = self.make_task(completed=True)
        response = self.client.post(
            reverse("tasks:toggle_task_completed", kwargs={"slug": task.slug})
        )
        task.refresh_from_db()

        self.assertFalse(task.completed)
        self.assertEqual(response.status_code, 302)

    def test_tasks_toggle_task_completed_view_get_request_does_not_change_task_status(
        self,
    ):
        task = self.make_task()
        response = self.client.get(
            reverse("tasks:toggle_task_completed", kwargs={"slug": task.slug})
        )
        task.refresh_from_db()

        self.assertFalse(task.completed)
        self.assertEqual(response.status_code, 302)

    def test_tasks_update_tasks_returns_error_message_when_form_is_invalid(self):
        task1 = self.make_task(title="Teste")
        task2 = self.make_task(title="Teste2")
        response = self.client.post(
            reverse("tasks:update_task", kwargs={"slug": task1.slug}),
            data={"title": task2.title},
        )

        content = response.content.decode("utf-8")
        self.assertIn("Essa tarefa já existe.", content)

    def test_tasks_update_tasks_redirects_to_task_detail_after_successful_update(self):
        task = self.make_task()

        response = self.client.post(
            reverse("tasks:update_task", kwargs={"slug": task.slug}),
            data={"title": "Updated Task", "start_date": task.start_date},
        )

        response.content.decode("utf-8")
        self.assertRedirects(
            response, reverse("tasks:task_detail", kwargs={"slug": "updated-task"})
        )

    def test_tasks_update_tasks_does_not_update_if_no_changes(self):
        task = self.make_task()

        response = self.client.post(
            reverse("tasks:update_task", kwargs={"slug": task.slug}),
            data={"title": task.title, "start_date": task.start_date},
        )

        self.assertRedirects(
            response, reverse("tasks:task_detail", kwargs={"slug": task.slug})
        )

    def test_tasks_delete_tasks_shows_message_confirmation_before_deletion(self):
        task = self.make_task()

        response = self.client.get(
            reverse("tasks:delete_task", kwargs={"slug": task.slug})
        )

        content = response.content.decode("utf-8")
        self.assertIn(
            f'Tem certeza que deseja excluir a tarefa "{task.title}"?', content
        )

    def test_tasks_delete_task_redirects_to_tasks_list_after_deletion(self):
        task = self.make_task()

        response = self.client.post(
            reverse("tasks:delete_task", kwargs={"slug": task.slug})
        )

        self.assertRedirects(response, reverse("tasks:tasks"))

    def test_tasks_only_user_can_access_views(self):
        self.client.logout()
        response = self.client.get(reverse("tasks:dashboard"))
        self.assertRedirects(response, reverse("authors:login") + "?next=/dashboard/")

        response = self.client.get(reverse("tasks:tasks"))
        self.assertRedirects(response, reverse("authors:login") + "?next=/tasks/")

        response = self.client.get(reverse("tasks:categories"))
        self.assertRedirects(response, reverse("authors:login") + "?next=/categories/")

        task = self.make_task()
        response = self.client.get(
            reverse("tasks:task_detail", kwargs={"slug": task.slug})
        )
        self.assertRedirects(
            response, reverse("authors:login") + f"?next=/tasks/details/{task.slug}/"
        )

        response = self.client.post(
            reverse("tasks:toggle_task_completed", kwargs={"slug": task.slug}),
            data={"completed": "completed"},
        )
        self.assertRedirects(
            response,
            reverse("authors:login") + f"?next=/tasks/details/{task.slug}/toggle/",
        )

        response = self.client.post(
            reverse("tasks:update_task", kwargs={"slug": task.slug}),
            data={"title": "Updated Task", "start_date": task.start_date},
        )
        self.assertRedirects(
            response, reverse("authors:login") + f"?next=/tasks/update/{task.slug}/"
        )

        response = self.client.post(
            reverse("tasks:delete_task", kwargs={"slug": task.slug})
        )
        self.assertRedirects(
            response, reverse("authors:login") + f"?next=/tasks/delete/{task.slug}/"
        )

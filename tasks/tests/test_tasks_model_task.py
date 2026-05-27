from django.core.exceptions import ValidationError
from parameterized import parameterized

from .test_base_tasks import TasksTestBase


class TasksTaskModelTests(TasksTestBase):
    def setUp(self):
        super().setUp()
        self.task = self.make_task(title="Work")

    def test_tasks_model_task_str_method(self):
        self.assertEqual(
            str(self.task),
            f"{self.task.title} - {'Completed' if self.task.completed else 'Not Completed'}",
        )

    @parameterized.expand(
        [
            ("title", 150),
        ]
    )
    def test_task_fields_max_lenght(self, field, max_lenght):
        setattr(self.task, field, "A" * (max_lenght + 1))
        with self.assertRaises(ValidationError):
            self.task.full_clean()

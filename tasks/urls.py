from django.urls import path

from .views import generic_views, views_category, views_tasks

app_name = "tasks"

urlpatterns = [
    path("", generic_views.home, name="home"),
    path("dashboard/", generic_views.dashboard, name="dashboard"),
    path("tasks/", views_tasks.task_list, name="tasks"),
    path("tasks/create/", views_tasks.CreateTask.as_view(), name="create_task"),
    path(
        "tasks/update/<slug:slug>/",
        views_tasks.UpdateTask.as_view(),
        name="update_task",
    ),
    path(
        "tasks/delete/<slug:slug>/",
        views_tasks.DeleteTask.as_view(),
        name="delete_task",
    ),
    path("tasks/details/<slug:slug>/", views_tasks.task_detail, name="task_detail"),
    path(
        "tasks/details/<slug:slug>/toggle/",
        views_tasks.toggle_task_completed,
        name="toggle_task_completed",
    ),
    path(
        "tasks/category/<slug:slug>/",
        views_tasks.tasks_by_category,
        name="tasks_by_category",
    ),
    path("categories/", views_category.category_list, name="categories"),
    path(
        "categories/create/",
        views_category.CreateCategory.as_view(),
        name="create_category",
    ),
    path(
        "categories/update/<slug:slug>/",
        views_category.UpdateCategory.as_view(),
        name="update_category",
    ),
    path(
        "categories/delete/<slug:slug>/",
        views_category.DeleteCategory.as_view(),
        name="delete_category",
    ),
]

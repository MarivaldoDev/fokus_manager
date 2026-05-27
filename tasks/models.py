from autoslug import AutoSlugField
from django.db import models
from django.utils.text import slugify

from authors.models import Author


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from="name", always_update=True)
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name="categories"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("author", "slug")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=150)
    slug = AutoSlugField(populate_from="title", always_update=True)
    description = models.TextField(max_length=300, blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="tasks", blank=True, null=True
    )
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="tasks")
    start_date = models.DateField()
    finish_date = models.DateField(blank=True, null=True)
    image = models.ImageField(upload_to="task_images/%Y/%m/", blank=True, null=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("author", "slug")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {'Completed' if self.completed else 'Not Completed'}"

import logging

from django.contrib.auth.models import AbstractUser
from django.db import models

logger = logging.getLogger(__name__)


class Author(AbstractUser):
    image_profile = models.ImageField(upload_to="author_images/%Y/%m/", blank=True, null=True)

    def __str__(self) -> str:
        return self.username

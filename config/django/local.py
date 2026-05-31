from pathlib import Path

from decouple import config

from .base import *  # noqa: F403

DEBUG = config("DEBUG", default=True, cast=bool)
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

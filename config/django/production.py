from decouple import config

from .base import *  # noqa: F403

DEBUG = config("DEBUG", default=False, cast=bool)
ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS",
    default="fokusmanager.online",
    cast=lambda v: [s.strip() for s in v.split(",")],
)

CSRF_TRUSTED_ORIGINS = [
    "https://fokusmanager.online",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": config("DB_HOST"),
        "PORT": config("DB_PORT", default="5432"),
        "OPTIONS": {
            "sslmode": "require",
        },
    }
}

DATABASES["default"]["CONN_MAX_AGE"] = 60


SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

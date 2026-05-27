import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
log_dir = os.path.join(BASE_DIR, "logs")
os.makedirs(log_dir, exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "[%(asctime)s] %(levelname)s %(name)s: %(message)s",
        },
        "colored": {
            "()": "colorlog.ColoredFormatter",
            "format": "%(log_color)s[%(levelname)s]%(reset)s %(blue)s%(name)s:%(reset)s %(message)s",
            "log_colors": {
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            },
        },
        "simple_format": {
            "format": "%(levelname)s | %(name)s | %(asctime)s | %(message)s | %(filename)s | %(lineno)d",
        },
    },
    "handlers": {
        "debug_file": {
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs/debug.log"),
            "level": "DEBUG",
            "formatter": "default",
        },
        "info_file": {
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs/info.log"),
            "level": "INFO",
            "formatter": "default",
        },
        "error_file": {
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs/error.log"),
            "level": "ERROR",
            "formatter": "simple_format",
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "colored",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "django.utils.autoreload": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "tasks": {
            "handlers": ["debug_file", "info_file", "error_file", "console"],
            "level": "DEBUG",
            "propagate": False,
        },
        "authors": {
            "handlers": ["debug_file", "info_file", "error_file", "console"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}

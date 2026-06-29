"""
Local development settings.
"""
from .base import *  # noqa: F403, F401

DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1", "localhost", "0.0.0.0"]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

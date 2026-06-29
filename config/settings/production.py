"""
Production environment settings.
"""
import os

from .base import *  # noqa: F403, F401

DEBUG = False

ALLOWED_HOSTS = os.environ.get(
    "DJANGO_ALLOWED_HOSTS",
    "sevendyne.com,www.sevendyne.com",
).split(",")

CSRF_TRUSTED_ORIGINS = os.environ.get(
    "CSRF_TRUSTED_ORIGINS",
    "https://sevendyne.com,https://www.sevendyne.com",
).split(",")

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


"""
Django Docker settings for Dreamjub project.
Reads all relevant setting from the environment
"""

from .settings import *
import sys

# No Debugging
DEBUG = False

# we want to allow all hosts
ALLOWED_HOSTS = os.environ.setdefault("DJANGO_ALLOWED_HOSTS", "").split(",")

# all our sessions be safe
SECRET_KEY = os.environ.setdefault("DJANGO_SECRET_KEY", "")


# Database
DATABASES = {
    'default': {
        'ENGINE': os.environ.setdefault("DJANGO_DB_ENGINE", ""),
        'NAME': os.environ.setdefault("DJANGO_DB_NAME", ""),
        'USER': os.environ.setdefault("DJANGO_DB_USER", ""),
        'PASSWORD': os.environ.setdefault("DJANGO_DB_PASSWORD", ""),
        'HOST': os.environ.setdefault("DJANGO_DB_HOST", ""),
        'PORT': os.environ.setdefault("DJANGO_DB_PORT", ""),
    }
}

# Static & Media URLs
STATIC_ROOT = "/var/www/static"
MEDIA_ROOT = "/data/media"
MEDIA_URL = "/media/"

# Email
# For the magic link login
EMAIL_BACKEND = os.environ.setdefault("EMAIL_BACKEND", "")
EMAIL_HOST = os.environ.setdefault("EMAIL_HOST", "")
EMAIL_PORT = int(os.environ.setdefault("EMAIL_PORT", ""))
EMAIL_HOST_USER = os.environ.setdefault("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.setdefault("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = os.environ.setdefault("EMAIL_USE_TLS", "") == "1"

# Sesame
SESAME_TOKEN_NAME = os.environ.setdefault("SESAME_TOKEN_NAME", "")
SESAME_MAX_AGE = int(os.environ.setdefault("SESAME_MAX_AGE", ""))


# Sentry
if os.environ.get('DJANGO_RAVEN_DSN'):
    # add sentry
    INSTALLED_APPS += (
        'raven.contrib.django.raven_compat',
    )

    import os
    import raven

    RAVEN_CONFIG = {
        'dsn': os.environ.get('DJANGO_RAVEN_DSN')
    }

import os

from .base import *

DEBUG = False

# Only allow the following hosts in production
DOMAIN_NAME = os.getenv("DOMAIN_NAME", "ztp.dev")
ALLOWED_HOSTS = [DOMAIN_NAME]

# Secret key must be more than 50 characters and more than 5 unique characters
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

# Use PostgreSQL for production
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
    }
}

# Security
CORS_ORIGIN_ALLOW_ALL = False
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# TODO: enforce https for keycloak host
# KEYCLOAK_URL = f"{KEYCLOAK_HOST}/auth/realms/{KEYCLOAK_REALM}"

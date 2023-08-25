from .base import *

DEBUG = True

# Allow all hosts in development
ALLOWED_HOSTS = ["*"]

# Allow all origins in development
CORS_ORIGIN_ALLOW_ALL = True
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False
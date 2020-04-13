from .base import *

SECRETS_DEV = SECRETS_FULL['dev']

DEBUG = True

WSGI_APPLICATION = 'config.wsgi.dev.application'

DATABASES = SECRETS_DEV['DATABASES']

ALLOWED_HOSTS += [
    '*',
]

# django-debug-toolbar
MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS = [
    '127.0.0.1',
]

INSTALLED_APPS += [
    'debug_toolbar',
    'django_extensions',
]

# Cross domain
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

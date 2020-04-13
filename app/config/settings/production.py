from .base import *

SECRETS_PRODUCTION = SECRETS_FULL['production']

DEBUG = False

WSGI_APPLICATION = 'config.wsgi.production.application'

DATABASES = SECRETS_PRODUCTION['DATABASES']
ALLOWED_HOSTS += [
    SECRETS_PRODUCTION['HOST'],
    'daangnmarket.shinjam.xyz',
]

# Cross domain
CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = ALLOWED_HOSTS

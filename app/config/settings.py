import os
import json
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = os.path.dirname(BASE_DIR)

# aad/.media
# User-uploaded static files의 기본 경로
MEDIA_ROOT = os.path.join(ROOT_DIR, '.media')
MEDIA_URL = '/media/'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '946wit_ka_)bsr412&@6xn6hkql6e=y($xm&830i!l6_!4w4a@'

SECRET_FILE = os.path.join(ROOT_DIR, 'secrets.json')

with open(SECRET_FILE) as json_file:
    data = json.load(json_file)
    # database
    DB_NAME = data['DB_NAME']
    DB_USER = data['DB_USER']
    DB_PASSWORD = data['DB_PASSWORD']
    DB_HOST = data['DB_HOST']
    # sentry
    SENTRY_DSN = data['SENTRY_DSN']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*', ]

# Application definition
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    # DRF
    'rest_framework',
    'rest_framework.authtoken',
]
THIRD_PARTY_APPS = [
    'import_export',
    'drf_yasg',
    'corsheaders',
    'push_notifications',
]
PROJECT_APPS = [
    'core.apps.CoreConfig',
    'location.apps.LocationConfig',
    'post.apps.PostConfig',
    'members.apps.MembersConfig',
    'notification'
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.contrib.gis.db.backends.postgis',
    #     'NAME': DB_NAME,
    #     'USER': DB_USER,
    #     'PASSWORD': DB_PASSWORD,
    #     'HOST': DB_HOST,
    #     'PORT': 5432,
    # },
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'db.daangn',
        'USER': 'jam',
        'HOST': 'localhost',
    },
}

# Cross domain
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
# CORS_ORIGIN_WHITELIST = []


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Auth User model
AUTH_USER_MODEL = 'members.User'
USER_MODEL = 'members.User'

# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(ROOT_DIR, 'staticfiles')

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

# django-debug-toolbar
INTERNAL_IPS = [
    '127.0.0.1',
]

INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

# Sentry
sentry_sdk.init(
    dsn=SENTRY_DSN,
    integrations=[DjangoIntegration()],

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)

# Swagger
SWAGGER_SETTINGS = {
    'DEFAULT_AUTO_SCHEMA_CLASS': 'core.swagger_custom.MyAutoSchema',
    'SECURITY_DEFINITIONS': {
        'Token': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        },
    }
}

# Django Push Notification
PUSH_NOTIFICATIONS_SETTINGS = {
    'FCM_API_KEY': 'AAAAFTwNi8I:APA91bGm57yBulML3oQEPQSezorzYzoyIr5v8YRmk4akotEFjxjInMnzmTwOVrl7DLCpQQiXifjrpB3nlFqT3H2hS9QBny25SCq8WuqV-xbIBcCuOgeiBpL_iDQBWbL1hfoLh1DiPmg-',
}

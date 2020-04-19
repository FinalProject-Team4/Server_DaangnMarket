import os
import json
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from core.utils import make_dir

BASE_DIR = make_dir(os.path.abspath(__file__), 3)
ROOT_DIR = make_dir(BASE_DIR)

with open(os.path.join(ROOT_DIR, 'secrets.json')) as json_file:
    SECRETS_FULL = json.load(json_file)
    SECRETS_BASE = SECRETS_FULL['base']
    SECRET_KEY = SECRETS_BASE['SECRET_KEY']
    SENTRY_DSN = SECRETS_BASE['SENTRY_DSN']

ALLOWED_HOSTS = []

# Application definition
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),

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
    'django_filters',
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

AUTHENTICATION_BACKENDS = [
    'core.my_auth.UserBackend',
    # 'django.contrib.auth.backends.ModelBackend',
]

# Internationalization

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True

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

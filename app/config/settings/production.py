from .base import *

SECRETS_PRODUCTION = SECRETS_FULL['production']

DEBUG = False

WSGI_APPLICATION = 'config.wsgi.production.application'

# aws settings
AWS_IAM_S3 = SECRETS_FULL['AWS_IAM_S3']

AWS_ACCESS_KEY_ID = AWS_IAM_S3['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = AWS_IAM_S3['AWS_SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME = AWS_IAM_S3['AWS_STORAGE_BUCKET_NAME']
AWS_DEFAULT_ACL = None
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
# s3 static settings
STATIC_LOCATION = 'static'
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'
STATICFILES_STORAGE = 'config.storage_backends.StaticStorage'

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

# s3 public media settings
PUBLIC_MEDIA_LOCATION = 'media'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/'
DEFAULT_FILE_STORAGE = 'config.storage_backends.PublicMediaStorage'

DATABASES = SECRETS_PRODUCTION['DATABASES']

ALLOWED_HOSTS += [
    SECRETS_BASE['HOST'],
    'daangnmarket.shinjam.xyz',
]

# Cross domain
CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = ALLOWED_HOSTS

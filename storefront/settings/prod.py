import os
import dj_database_url
from .common import *

DEBUG = False

SECRET_KEY = os.environ.get('SECRET_KEY')

ALLOWED_HOSTS = ['suuqcasri-production-839407217d71.herokuapp.com']

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config()
}

REDIS_URL = os.environ.get('REDISCLOUD_URL', 'redis://localhost:6379')


CELERY_BROKER_URL = REDIS_URL   

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

EMAIL_HOST = os.environ.get('MAILGUN_SMTP_SERVER')
EMAIL_HOST_USER = os.environ.get('MAILGUN_SMTP_LOGIN')
EMAIL_HOST_PASSWORD = os.environ.get('MAILGUN_SMTP_PASSWORD')
EMAIL_PORT = os.environ.get('MAILGUN_SMTP_PORT')

# Cloud Storage configuration

AWS_ACCESS_KEY_ID = os.environ.get('DO_SPACES_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = os.environ.get('DO_SPACES_SECRET_KEY')
AWS_STORAGE_BUCKET_NAME = 'suuqcasri-storage'
AWS_S3_REGION_NAME = 'nyc3'
AWS_S3_ENDPOINT_URL = 'https://nyc3.digitaloceanspaces.com'

AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.nyc3.digitaloceanspaces.com'

STORAGES = {
    'default': {
        'BACKEND': 'storefront.storage_backends.MediaStorage'
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    }
}

MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
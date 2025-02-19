import os
import dj_database_url
from .common import *

DEBUG = False

SECRET_KEY = os.environ.get('SECRET_KEY')

ALLOWED_HOSTS = ['suuqcasri-prod-b2dbb1ea4f1e.herokuapp.com']

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



GS_BUCKET_NAME = os.environ.get('GS_BUCKET_NAME')


GS_PROJECT_ID = os.environ.get('GS_PROJECT_ID')



DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'

MEDIA_URL = f'https://storage.googleapis.com/{GS_BUCKET_NAME}/'
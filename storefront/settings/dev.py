
from .common import *

DEBUG = True

SECRET_KEY = 'django-insecure-4mdu07=ww!@(vjdhokn=chk)gv*2i6)0^r7b^n20e%lc(twh%d'

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'storefront',
        'HOST': 'localhost',
        'USER': 'root',
        'PASSWORD': 'Software'
    }
}


if DEBUG:
    MIDDLEWARE += ['silk.middleware.SilkyMiddleware']


CELERY_BROKER_URL = 'redis://localhost:6379/1'    
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

EMAIL_HOST = 'localhost'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 2525

MEDIA_URL = '/media/'
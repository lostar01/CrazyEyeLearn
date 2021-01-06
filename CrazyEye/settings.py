"""
Django settings for CrazyEye project.

Generated by 'django-admin startproject' using Django 3.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os
# import djcelery

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*18d1&ig4fukhc2x=)nv+y#c*#kbb*43ypxj%zzgqocj5!_a%t'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'web',
    'channels',
    # 'djcelery',  # django-celery only support 1.1 to django=2.2
    'django_celery_beat',
]

ASGI_APPLICATION='web.routing.application'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'CrazyEye.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'CrazyEye.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

LOGIN_URL = '/login/'
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
AUDIT_LOG_DIR = '%s/var/audit_log' %(BASE_DIR)
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

AUTH_USER_MODEL = 'web.UserProfile'
WEB_SSH_URL="http://192.168.137.170:8888"

# define private key temp dir
TMP_DIR = '/tmp'

#page paging count peer page
PER_PAGE_COUNT = 10

# config celery
BROKER_URL='redis://:mydev_redis01@192.168.137.170:6379/2'

#config store the result
CELERY_RESULT_BACKEND = 'redis://:mydev_redis01@192.168.137.170:6379/2'

#config connection timeout
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 43200}

#config message formater
CELERY_ACCEPT_CONNECT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'

#config celery timezone
CELERY_TIMEZONE = TIME_ZONE

# djcelery.setup_loader()
# CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
#config celery_beat
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

# CELERY_DEFAULT_EXCHANGE = 'celery'
# CELERY_DEFAULT_EXCHANGE_TYPE = 'direct'
# CELERY_DEFAULT_QUEUE = 'celery'
# CELERY_DEFAULT_ROUTING_KEY = 'celery'
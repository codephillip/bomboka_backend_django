"""
Django settings for bomboka_backend project.

Generated by 'django-admin startproject' using Django 1.10.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# todo replace with production secret
SECRET_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1MDMzOTI4OTEsImVtYWlsIjoiS3J1a292N0BleGFtcGxlLmNvbSIsInVzZXJfaWQiOiI4YWZlYWViYS1jNDYzLTQyN2MtYTNjMC0yN2JlMTAwY2UxNDEiLCJvcmlnX2lhdCI6MTUwMzM4OTI5MSwidXNlcm5hbWUiOiJLcnVrb3Y3S3J1a292NyJ9.VqaAFsoi5CE8MSYuTWbglqZuTWRmU-rwAhToApYcJWg'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# todo restrict hosts on launch
ALLOWED_HOSTS = ['*']

# todo access on launch
CORS_ORIGIN_ALLOW_ALL = True

# todo activate on launch
# CORS_ORIGIN_WHITELIST = (
#     '127.0.0.1:8080',
#     'localhost:8080',
#     'hostname.example.com'
# )

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapp',
    'rest_framework',
    'rest_framework_swagger',
    'rest_framework.authtoken',
    'djoser',
    'django_filters',
    'corsheaders'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'bomboka_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'bomboka_backend.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = 'myapp.User'

REST_FRAMEWORK = {
    # todo activate on launch
    # 'DEFAULT_RENDERER_CLASSES': (
    #     'rest_framework.renderers.JSONRenderer',
    # ),
    # 'DEFAULT_PARSER_CLASSES': (
    #     'rest_framework.parsers.JSONParser',
    # ),
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        # 'rest_framework.permissions.IsAuthenticated',
        # debugging only. to allow access to the api without tokens
        'rest_framework.permissions.AllowAny',
        # 'rest_framework.permissions.IsAdminUser',
    ),
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.PageNumberPagination',
        'PAGE_SIZE': 100,
}

JWT_AUTH = {
    'JWT_SECRET_KEY': SECRET_KEY,
    'JWT_VERIFY': True,
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_LEEWAY': 0,
    # user is logged in for 1 hour before token expires
    'JWT_EXPIRATION_DELTA': datetime.timedelta(hours=6),
    'JWT_ALLOW_REFRESH': True,
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),
}

DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL': 'password/insert_new_password/{uid}/{token}',
    'ACTIVATION_URL': '#/activate/{uid}/{token}',
    'SERIALIZERS': {
        'user_registration': 'myapp.serializers.UserPostSerializer',
    },
}

# todo update credentials, use bomboka smtp server
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
# todo replace with info@bomboka.com
EMAIL_HOST_USER = 'codephillip@gmail.com'
EMAIL_HOST_PASSWORD = 'createNEWpassw07d'
EMAIL_PORT = 587

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'bomboka_backend/static'),
)

MEDIA_ROOT = "photos/"
if DEBUG:
    MEDIA_URL = 'http://127.0.0.1:8000/photos/'
else:
    pass
    # TODO add server endpoint

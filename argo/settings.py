# -*- encoding: utf-8 -*-

import os
from decouple import config
from unipath import Path
import dj_database_url
import django_heroku

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = Path(__file__).parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='S#perS3crEt_1122')

# SECURITY WARNING: don't run with debug turned on in production!
#  DEBUG = config('DEBUG', default=False)
DEBUG = True

# load production server from .env
ALLOWED_HOSTS = ['localhost', '127.0.0.1', config('SERVER', default='127.0.0.1')]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'compressor',
    'frontend.apps.FrontendConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'argo.urls'
LOGIN_REDIRECT_URL = "home_page"
LOGOUT_REDIRECT_URL = "home_page"
TEMPLATE_DIR = os.path.join(BASE_DIR, "frontend/templates")

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
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
WSGI_APPLICATION = 'argo.wsgi.application'

# Database
DATABASES = {}
DATABASES['default'] = dj_database_url.config(conn_max_age=600)
db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(db_from_env)

# Password validation
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

#############################################################
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'frontend/static'),
)


CRISPY_TEMPLATE_PACK="bootstrap4"
LOGIN_REDIRECT_URL = '/account/'
LOGOUT_REDIRECT_URL = '/'
TAGGIT_CASE_INSENSITIVE = True


#  MEDIA_URL = "/media/"
#  MEDIA_ROOT = path.join(BASE_DIR, 'media')
#  STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
#  STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
#  STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
#  STATICFILES_STORAGE = 'cloudinary_storage.storage.StaticHashedCloudinaryStorage'

#  EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
#  EMAIL_FILE_PATH = str(BASE_DIR.joinpath('sent_emails'))
#  EMAIL_HOST = 'smtp.sendgrid.net'
#  EMAIL_HOST_USER = 'EMAIL_HOST_USER'
#  EMAIL_HOST_PASSWORD = 'EMAIL_HOST_PASSWORD'
#  EMAIL_PORT = 587
#  EMAIL_USE_TLS = True

#  SECURE_BROWSER_XSS_FILTER = True
#  X_FRAME_OPTIONS = 'DENY'
#  SECURE_SSL_REDIRECT = True
#  SECURE_HSTS_SECONDS = 3600
#  SECURE_HSTS_INCLUDE_SUBDOMAINS = True
#  SECURE_HSTS_PRELOAD = True
#  SECURE_CONTENT_TYPE_NOSNIFF = True
#  SESSION_COOKIE_SECURE = True
#  CSRF_COOKIE_SECURE = True
#  SECURE_REFERRER_POLICY = 'same-origin'
#  options = DATABASES['default'].get('OPTIONS', {})
#  options.pop('sslmode', None)

#  dotenv_file = path.join(BASE_DIR, ".env")
#  if path.isfile(dotenv_file):
    #  dotenv.load_dotenv(dotenv_file)

django_heroku.settings(locals())

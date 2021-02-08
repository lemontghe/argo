from pathlib import Path
from os import path, environ
import dj_database_url
import dotenv
import django_heroku

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False 
#  DEBUG = False
#  ALLOWED_HOSTS = ["example.com", "localhost"]
ALLOWED_HOSTS = ["argooo.herokuapp.com", "127.0.0.1", "0.0.0.0"]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'frontend.apps.FrontendConfig',
    #  'api.apps.ApiConfig',
    #  'rest_framework',
    'compressor',
    'crispy_forms',
    'django.contrib.sites',
    'whitenoise.runserver_nostatic',
]

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #  'whitenoise.runserver_nostatic',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'argo.urls'
SITE_ID=1,

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

WSGI_APPLICATION = 'argo.wsgi.application'

# Database

#  DATABASES = {
    #  'default': {
        #  'ENGINE': 'django.db.backends.sqlite3',
        #  'NAME': BASE_DIR / 'db.sqlite3',
    #  }
#  }

#  DATABASES = {
    #  'default': {
        #  'ENGINE': 'django.db.backends.postgresql_psycopg2',
        #  'NAME': 'd3s5298qa0cop7',
        #  'USER': 'jnuyfonzyaieps',
        #  'PASSWORD': '078ac3c17b66e0fa6581c5019990dc61f31ff511ba499d73151db99d21a35722',
        #  'HOST': 'ec2-52-205-3-3.compute-1.amazonaws.com',
        #  'PORT': '5432',
    #  }
#  }


#  DATABASES = {
    #  'default': {
        #  'ENGINE': 'django.db.backends.mysql',
        #  'NAME': 'argo',
        #  'USER': 'user',
        #  'PASSWORD': 'pass',
        #  'HOST':'sql202.dwwdd.com',
        #  'PORT': '3306',
    #  }
#  }


#  db_from_env = dj_database_url.config(conn_max_age=600)
#  DATABASES['default'].update(db_from_env)

DATABASES = {}
DATABASES['default'] = dj_database_url.config(conn_max_age=600)

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


STATIC_URL = '/static/'
STATIC_ROOT = path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = (
    path.join(BASE_DIR, 'static'),
)

MEDIA_URL = "/media/"
MEDIA_ROOT = path.join(BASE_DIR, 'media')
#  STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
#  STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'



CRISPY_TEMPLATE_PACK="bootstrap4"
LOGIN_REDIRECT_URL = '/account/'
LOGOUT_REDIRECT_URL = '/'
TAGGIT_CASE_INSENSITIVE = True
#  EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
#  EMAIL_FILE_PATH = str(BASE_DIR.joinpath('sent_emails'))

#  EMAIL_HOST = 'smtp.sendgrid.net'
#  EMAIL_HOST_USER = 'EMAIL_HOST_USER'
#  EMAIL_HOST_PASSWORD = 'EMAIL_HOST_PASSWORD'
#  EMAIL_PORT = 587
#  EMAIL_USE_TLS = True

dotenv_file = path.join(BASE_DIR, ".env")
if path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

django_heroku.settings(locals())
options = DATABASES['default'].get('OPTIONS', {})
options.pop('sslmode', None)

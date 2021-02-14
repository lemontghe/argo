from pathlib import Path
from os import path, environ
import dj_database_url
import dotenv
import django_heroku

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = "SECRET_KEY"
#  SECRET_KEY = environ.get('SECRET_KEY')

DEBUG = True
#  DEBUG = False
ALLOWED_HOSTS = ['localhost', '127.0.0.1',"argooo.herokuapp.com"]
#  ALLOWED_HOSTS = ["argooo.herokuapp.com", "0.0.0.0"]
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'frontend.apps.FrontendConfig',
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
        #  'NAME': 'argo',
        #  'USER': 'argo',
        #  'PASSWORD': 'pass',
        #  'HOST': 'adkfal',
        #  'PORT': '5432',
    #  }
#  }

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
#  STATICFILES_STORAGE = 'cloudinary_storage.storage.StaticHashedCloudinaryStorage'

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
options = DATABASES['default'].get('OPTIONS', {})
options.pop('sslmode', None)

SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SECURE = True 
CSRF_COOKIE_SECURE = True 
SECURE_REFERRER_POLICY = 'same-origin'

#  django_heroku.settings(config=locals(), staticfiles=False,logging=False)
django_heroku.settings(locals())

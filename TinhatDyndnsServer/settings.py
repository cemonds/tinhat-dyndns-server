"""
Django settings for TinhatDyndnsServer project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^59+5!vq0%fv#+e!j7yn^y+2p0dl8pt3t^-oi4$1rjskax-gqm'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'restapi',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'restapi.error.ErrorMiddleware',
)

ROOT_URLCONF = 'TinhatDyndnsServer.urls'

WSGI_APPLICATION = 'TinhatDyndnsServer.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'


# Settings for the dyndns service
LOCAL_DIR = os.path.abspath(os.path.dirname(__name__)) # needs to be set!

SUDO_NSD_CONTROL = False
NSD_CONTROL_PATH = None
GPG_PATH = '"C:\\Program Files (x86)\\GNU\\GnuPG\\gpg.exe"'

ZONES_DIRECTORY = os.path.join(LOCAL_DIR, 'zones')
TEMPLATE_DIRS  = (os.path.join(LOCAL_DIR, 'templates').replace(os.path.sep, '/'),) # Needs / even on windows
KEYS_DIRECTORY = os.path.join(LOCAL_DIR, 'keys')

ZONE_TEMPLATE = 'template.zone'
ZONES_PATTERN = 'dynamic'
ZONE_DOMAIN = 's.tinhat.de'

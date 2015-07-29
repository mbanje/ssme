"""
Django settings for ssme project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))




PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                            os.pardir))
PROJECT_ROOT = os.path.abspath(os.path.join(PROJECT_PATH, os.pardir))

TEMPLATE_DIRS = (
     os.path.join(PROJECT_PATH, 'templates'),
)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/


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
	'ssme_activities',
	'django_tables2',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)




TEMPLATE_CONTEXT_PROCESSORS = (
	'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',

)






ROOT_URLCONF = 'ssme.urls'

WSGI_APPLICATION = 'ssme.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#    }
#}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Bujumbura'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(PROJECT_PATH,  'media')

MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(PROJECT_PATH,  'static')


DOCUMENT_ROOT = PROJECT_PATH


STATICFILES_DIRS = (
    os.path.join(PROJECT_PATH, 'staticfiles'),
)


# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

KNOWN_PREFIXES = {
'SDJ':'StockDebutJourneeControler',
'sdj':'StockDebutJourneeControler',
'SR':'StockRecuLeMatinControler',
'sr':'StockRecuLeMatinControler',
'SF':'StockFinalControler',
'sf':'StockFinalControler',
'B':'BeneficiairesControler',
'b':'BeneficiairesControler',
'RS':'RuptureStockControler',
'FRS':'FinRuptureStockControler',
}

VARIABLE_NUMBER = {
'SDJ':9,
'SR':7,
'SF':7,
'B':9,
'RS':3,
'FRS':3,
}


try:
    from localsettings import *
except ImportError:
    pass

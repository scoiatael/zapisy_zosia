# Django settings for zapisy_zosia project.
#-*- coding: utf-8 -*- 
import os, sys 
from os.path import abspath, dirname, join 
 
 
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__)) 


DEBUG = True
TEMPLATE_DEBUG = DEBUG
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
    ('Maciek', 'xberus@gmail.com')
)

MANAGERS = ADMINS

DATABASES = {
     'default' : {
        'ENGINE' : 'django.db.backends.sqlite3',
 	    'NAME' : os.path.join(PROJECT_PATH, 'db.sqlite3'),
 	    'PORT' : '',
 	    'USER' : '',
	    'PASSWORD' : '',
 	    'HOST' : '',
 	    'CHARSET' : 'utf8',
 	    'USE_UNICODE' : True,
        }
}

# Local time zone for this installation. Choices can be found here:
# http://www.postgresql.org/docs/8.1/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
# although not all variations may be possible on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'CET'

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
# http://blogs.law.harvard.edu/tech/stories/storyReader$15
LANGUAGE_CODE = 'pl'
LANGUAGES = (
    ('pl', 'Polish'),
)
LOCALE_PATHS = (os.path.join(PROJECT_ROOT, 'locale'),)
SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'static_media')

# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"
#MEDIA_URL = '/site_media'
STATIC_URL = '/static/'


# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '^(*+wz_l2paerc)u(si)-a#aotpk#6___9e*o4(_0tlegdmfl+'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (

    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
     )),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'sponsors.processors.sponsors'
)

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, 'templates'),
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    #'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.formtools',
    'rooms',
    'lectures',
    'blog',
    'common',
    'blurb',
    'south',
    'users',
    'sponsors',
    'polls',
    'django_extensions',
)

#AUTHENTICATION_BACKENDS = (
#    'email-auth.EmailBackend',
#)

# well, it's temporary, of course...
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '25'
EMAIL_HOST_USER = 'zosia.xxxx@gmail.com' # it doesn't exist afaik
EMAIL_HOST_PASSWORD = 'haselko'
EMAIL_USE_TLS = True

CACHE_BACKEND = 'locmem:///'
CACHE_MIDDLEWARE_SECONDS = 30

SESSION_ENGINE = "django.contrib.sessions.backends.file"


try:
    from settings_local import *
except ImportError:
    pass

AUTH_USER_MODEL = 'users.Participant'
import os

# Make sure you set the following configuration environment variables:
#
#   STREETSCORE_COMPRESS_ENABLED ('True', or 'False')
#
#   DATABASE_URL
#     - or -
#   STREETSCORE_DB_NAME
#   STREETSCORE_DB_USER
#   STREETSCORE_DB_PASS
#   STREETSCORE_DB_HOST
#   STREETSCORE_DB_PORT
#


try:
    import local
except ImportError:
    local = None

try:
    import json

    # If on DotCloud...
    with open('/home/dotcloud/environment.json') as f:
        # Load the dotcloud environment file into memory.
        env = json.load(f)

except IOError:

    # If on Heroku...
    if 'DATABASE_URL' in os.environ:
        import sys
        import urlparse

        # Register database schemes in URLs.
        urlparse.uses_netloc.append('postgres')
        urlparse.uses_netloc.append('mysql')

        url = urlparse.urlparse(os.environ['DATABASE_URL'])

        # Update with environment configuration.
        env = {
            'STREETSCORE_DB_NAME': url.path[1:],
            'STREETSCORE_DB_USER': url.username,
            'STREETSCORE_DB_PASS': url.password,
            'STREETSCORE_DB_HOST': url.hostname,
            'STREETSCORE_DB_PORT': url.port or 5432,
        }
    else:
        env = {}

def abs_dir(sub_path):
    this_dir = os.path.dirname(__file__)
    return os.path.join(this_dir, '..', sub_path)

# Django settings for project project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME':     os.environ.get('STREETSCORE_DB_NAME', env.get('STREETSCORE_DB_NAME', 'streetscore')),                      # Or path to database file if using sqlite3.
        'USER':     os.environ.get('STREETSCORE_DB_USER', env.get('STREETSCORE_DB_USER', 'postgres')),                      # Not used with sqlite3.
        'PASSWORD': os.environ.get('STREETSCORE_DB_PASS', env.get('STREETSCORE_DB_PASS', 'postgres')),                  # Not used with sqlite3.
        'HOST':     os.environ.get('STREETSCORE_DB_HOST', env.get('STREETSCORE_DB_HOST', 'localhost')),                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT':     int(os.environ.get('STREETSCORE_DB_PORT', env.get('STREETSCORE_DB_PORT', '5432'))),                      # Set to empty string for default. Not used with sqlite3.
    }
}
if local:
    DATABASES.update(local.DATABASES)

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = '/home/dotcloud/data/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = '/home/dotcloud/data/static/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
    'compressor.finders.CompressorFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = local.SECRET_KEY if local else os.environ.get('STREETSCORE_SECURITY_KEY', env.get('STREETSCORE_SECRET_KEY', '12345'))

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

INTERNAL_IPS = ('127.0.0.1',)

ROOT_URLCONF = 'project.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'project.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #'django.contrib.gis',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',

    # 3rd-party reusable apps
    'south',
    'bootstrapped',
    'mustachejs',
    'djangorestframework',
    'backbonejs',
    'debug_toolbar',
    'django_nose',
    'compressor',
    'bulkadmin',

    # Project-specific apps
    'project',
)

# Only enable compression via an environment variable since the
# static/media directories are dotcloud specific at the moment.
COMPRESS_ENABLED = (os.environ.get('STREETSCORE_COMPRESS_ENABLED', env.get('STREETSCORE_COMPRESS_ENABLED', 'False')) == 'True')

SOUTH_TESTS_MIGRATE = False

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
SOUTH_AUTO_FREEZE_APP = True

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

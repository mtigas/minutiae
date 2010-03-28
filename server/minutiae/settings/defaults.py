import os
SETTINGS_DIR = os.path.dirname(os.path.abspath(__file__))
DJANGO_SERVER_DIR = os.path.join(SETTINGS_DIR,'..','..','..')

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = ()
MANAGERS = ()
INTERNAL_IPS = ()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.abspath(os.path.join(SETTINGS_DIR,'..','database.db')),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': ''
    }
}
SECRET_KEY = 'change me in server-specific secret_settings.py'

CACHE_BACKEND = 'dummy:///'
CACHE_MIDDLEWARE_SECONDS = 30
CACHE_MIDDLEWARE_KEY_PREFIX = "2miketigas_middleware"
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True
NGINX_CACHE_PREFIX = "NGINX_mt2"

TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False

# ===== Apps/app backend =====
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.comments',
    'django.contrib.contenttypes',
    #'django.contrib.flatpages',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'django.contrib.syndication',
    'contact_form',
    'typogrify',

    'minutiae.blog',
)

ROOT_URLCONF = 'minutiae.urls'

MIDDLEWARE_CLASSES = (
    #'cacheutil.middleware.NginxMemcacheMiddleWare',
    #'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    #'django.middleware.cache.FetchFromCacheMiddleware',
    #'minutiae.middleware.SuperuserSSLRedirect',
)

# ===== Media =====
MEDIA_ROOT = os.path.join(DJANGO_SERVER_DIR, 'static')
MEDIA_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/admin_media/'

# ===== Templates =====
TEMPLATE_DIRS = (
    os.path.join(DJANGO_SERVER_DIR, 'templates'),
)

TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.media",
    "django.contrib.messages.context_processors.messages"
)

# ===== Comments =====
COMMENT_MAX_LENGTH = 15000
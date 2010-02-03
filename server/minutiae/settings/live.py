from defaults import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

SEND_BROKEN_LINK_EMAILS = True

CACHE_BACKEND = 'memcached://127.0.0.1:11211/?timeout=259200&max_entries=100000&cull_frequency=5'
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

SERVER_EMAIL = 'server@miketigas.com'
DEFAULT_FROM_EMAIL = SERVER_EMAIL

MEDIA_URL = 'https://mtigas1.appspot.com/'
ADMIN_MEDIA_PREFIX = 'https://mtigas1.appspot.com/admin_media/'
#MEDIA_URL = 'http://media3.mike.tig.as/'
#ADMIN_MEDIA_PREFIX = 'http://media3.mike.tig.as/admin_media/'

MIDDLEWARE_CLASSES = (
    'cacheutil.middleware.NginxMemcacheMiddleWare',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'minutiae.middleware.SuperuserSSLRedirect',
)


# ADMINS
# MANAGERS
# CONTACT_FORM_RECIPIENTS
# (Above three for the sake of reducing spam)

# DATABASES
# EMAIL_HOST
# EMAIL_PORT
# EMAIL_HOST_USER 
# EMAIL_HOST_PASSWORD
# SECRET_KEY
try:
    from secret_settings import *
except:
    pass
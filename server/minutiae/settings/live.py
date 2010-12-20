from defaults import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

SEND_BROKEN_LINK_EMAILS = True

#CACHE_BACKEND = 'newcache://127.0.0.1:11211/?timeout=43200&max_entries=100000&cull_frequency=5&binary=1'
CACHE_BACKEND = 'memcached://127.0.0.1:11211/?timeout=43200&max_entries=100000&cull_frequency=5&binary=1'

PYLIBMC_BEHAVIORS = {
    'tcp_nodelay' : True,
    'no_block' : True,
    'connect_timeout': 150,
}
CACHE_VERSION = 3
FLAVOR = "miketigas.com"

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
SESSION_COOKIE_AGE = 43200
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

SERVER_EMAIL = 'server@miketigas.com'
DEFAULT_FROM_EMAIL = SERVER_EMAIL

MEDIA_URL = 'https://mtigas1.appspot.com/'
ADMIN_MEDIA_PREFIX = 'https://mtigas1.appspot.com/admin_media/'

MIDDLEWARE_CLASSES = (
    'cacheutil.middleware.NginxMemcacheMiddleWare',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'minutiae.middleware.SetRemoteAddrFromForwardedFor',
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
# AKISMET_API_KEY
try:
    from secret_settings import *
except:
    pass

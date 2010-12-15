from django.db.models import Model as DjangoModel
from django.core.cache import cache

try:
    from newcache import CacheClass as newcache_CacheClass
    using_newcache = issubclass(cache.__class__, newcache_CacheClass)
except:
    using_newcache = False

from hashlib import md5

# Make this compatible with django-newcache and Django 1.3 (which has support for key hashing)
from django.conf import settings
FLAVOR = getattr(settings, 'FLAVOR', '')
CACHE_VERSION = str(getattr(settings, 'CACHE_VERSION', 1))

# Faster than default newcache.get_key since it only coerces to string (utf-8) if it's given a unicode
# and uses the significantly CPU-faster md5
def get_key(cachename):
    # 3.6 to 4.4 usec/pass
    if type(cachename) == unicode:
        key = cachename.encode('utf-8')
    else:
        key = cachename
    
    hashed = md5(key).hexdigest()
    return ''.join((FLAVOR, '-', str(CACHE_VERSION), '-', hashed))

# compatibility with older code we have
def _get_real_cachename(cachename):
    from warnings import warn
    warn('_get_real_cachename() is now get_key()',DeprecationWarning, stacklevel=2)
    
    if using_newcache:
        return cachename
    else:
        return get_key(cachename)

def safe_get_cache(cachename):
    """ Gets an item from the cache (converting the given string into an always valid cache key) """
    
    # django-newcache will perform _get_real_cachename internally
    if using_newcache:
        key = cachename
    else:
        key = get_key(cachename)
    
    return cache.get(key)

def safe_set_cache(cachename, obj, timeout=None):
    """ Puts an item into the cache (converting the given string into an always valid cache key) """
    
    if using_newcache:
        key = cachename
    else:
        key = get_key(cachename)
    
    cache.set(
        key,
        obj,
        timeout
    )
    return obj

def safe_del_cache(cachename):
    """ Deletes an item from the cache (converting the given string into an always valid cache key) """
    if using_newcache:
        key = cachename
    else:
        key = get_key(cachename)
    
    cache.delete(key)

# The following are based on work from http://fi.am/entry/low-level-cache-decorators-for-django/
def cached_method(func, cachetime=None):
    """ Decorator for plain methods """
    def cached_func(*args, **kwargs):
        key = 'cached_method_%s_%s_%s' % \
            (func.__name__, hash(args), hash(frozenset(kwargs.items())))
        val = safe_get_cache(key)
        return safe_set_cache(key, func(*args, **kwargs), cachetime) if val is None else val
    return cached_func

# INCORRECTLY NAMED: this is actually an "instance method" decorator
def cached_clsmethod(func, cachetime=None):
    """ Decorator for instance methods """
    def cached_func(self, *args, **kwargs):
        if issubclass(self.__class__, DjangoModel):
            clsname = "%s.%s" % (self.__class__._meta.app_label, self.__class__.__name__)
        else:
            clsname = self.__class__.__name__
        
        key = 'cached_clsmethod_%s_%s_%s_%s_%s' % \
            (clsname, func.__name__, getattr(self,'pk',hash(self)), hash(args), hash(frozenset(kwargs.items())))
        
        val = safe_get_cache(key)
        return safe_set_cache(key, func(self, *args, **kwargs), cachetime) if val is None else val
    return cached_func

def cached_klsmethod(func, cachetime=None):
    """ Decorator for class methods """
    def cached_func(cls, *args, **kwargs):
        if issubclass(cls, DjangoModel):
            clsname = "%s.%s" % (cls._meta.app_label, cls.__name__)
        else:
            clsname = cls.__name__
        
        key = 'cached_clsmethod_%s_%s_%s_%s_%s' % \
            (clsname, func.__name__, hash(cls), hash(args), hash(frozenset(kwargs.items())))
        
        val = safe_get_cache(key)
        return safe_set_cache(key, func(cls, *args, **kwargs), cachetime) if val is None else val
    return classmethod(cached_func)

def cached_property(func, cachetime=None):
    """ Decorator for class properties """
    def cached_func(self):
        if issubclass(self.__class__, DjangoModel):
            clsname = "%s.%s" % (self.__class__._meta.app_label, self.__class__.__name__)
        else:
            clsname = self.__class__.__name__
        
        key = 'cached_property_%s_%s_%s' % \
            (clsname, func.__name__, getattr(self,'pk',hash(self)))
        
        val = safe_get_cache(key)
        return safe_set_cache(key, func(self), cachetime) if val is None else val
    return property(cached_func)

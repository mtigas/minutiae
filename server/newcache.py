"Modified memcached cache backend"

import time

from threading import local

from django.core.cache.backends.base import BaseCache, InvalidCacheBackendError
from django.utils.hashcompat import md5_constructor
from django.conf import settings

try:
    import pylibmc as memcache
    NotFoundError = memcache.NotFound
    using_pylibmc = True
except ImportError:
    using_pylibmc = False
    try:
        import memcache
        NotFoundError = ValueError
    except ImportError:
        raise InvalidCacheBackendError('Memcached cache backend requires ' + 
            'either the "pylibmc" or "memcache" library')

# Flavor is used amongst multiple apps to differentiate the "flavor" of the
# environment. Examples of flavors are 'prod', 'staging', 'dev', and 'test'.
FLAVOR = getattr(settings, 'FLAVOR', '')

CACHE_VERSION = str(getattr(settings, 'CACHE_VERSION', 1))
CACHE_BEHAVIORS = getattr(settings, 'CACHE_BEHAVIORS', {'hash': 'crc'})
CACHE_KEY_MODULE = getattr(settings, 'CACHE_KEY_MODULE', 'newcache')
CACHE_HERD_TIMEOUT = getattr(settings, 'CACHE_HERD_TIMEOUT', 60)

class Marker(object):
    pass

MARKER = Marker()

def get_key(cachename, flavor=FLAVOR, version=CACHE_VERSION):
    """
    Returns a hashed, versioned, flavored version of the string that was input.
    """
    if type(cachename) == unicode:
        key = cachename.encode('utf-8')
    else:
        key = cachename
    
    hashed = md5_constructor(key).hexdigest()
    return ''.join((flavor, '-', str(version), '-', hashed))

KEY_FUNC = get_key

class CacheClass(BaseCache):

    def __init__(self, server, params, key_prefix=FLAVOR, version=CACHE_VERSION, key_func=None):
        if not key_func:
            key_func = KEY_FUNC
        
        super(CacheClass, self).__init__(params, key_prefix, version, key_func)
        self._servers = server.split(';')
        self._use_binary = bool(params.get('binary'))
        self._local = local()
    
    @property
    def _cache(self):
        """
        Implements transparent thread-safe access to a memcached client.
        """
        client = getattr(self._local, 'client', None)
        if client:
            return client
        
        # Use binary mode if it's both supported and requested
        if using_pylibmc and self._use_binary:
            client = memcache.Client(self._servers, binary=True)
        else:
            client = memcache.Client(self._servers)
        
        # If we're using pylibmc, set the behaviors according to settings
        if using_pylibmc:
            client.behaviors = CACHE_BEHAVIORS
        
        self._local.client = client
        return client

    def _pack_value(self, value, timeout):
        """
        Packs a value to include a marker (to indicate that it's a packed
        value), the value itself, and the value's timeout information.
        """
        herd_timeout = (timeout or self.default_timeout) + int(time.time())
        return (MARKER, value, herd_timeout)
    
    def _unpack_value(self, value, default=None):
        """
        Unpacks a value and returns a tuple whose first element is the value,
        and whose second element is whether it needs to be herd refreshed.
        """
        try:
            marker, unpacked, herd_timeout = value
        except (ValueError, TypeError):
            return value, False
        if not isinstance(marker, Marker):
            return value, False
        if herd_timeout < int(time.time()):
            return unpacked, True
        return unpacked, False

    def _get_memcache_timeout(self, timeout):
        """
        Memcached deals with long (> 30 days) timeouts in a special
        way. Call this function to obtain a safe value for your timeout.
        """
        if timeout is None:
            timeout = self.default_timeout
        if timeout > 2592000: # 60*60*24*30, 30 days
            # See http://code.google.com/p/memcached/wiki/FAQ
            # "You can set expire times up to 30 days in the future. After that
            # memcached interprets it as a date, and will expire the item after
            # said date. This is a simple (but obscure) mechanic."
            #
            # This means that we have to switch to absolute timestamps.
            timeout += int(time.time())
        return timeout

    def add(self, key, value, timeout=None, version=None, herd=True):
        # If the user chooses to use the herd mechanism, then encode some
        # timestamp information into the object to be persisted into memcached
        if herd and timeout != 0:
            if timeout is None:
                timeout = self.default_timeout
            packed = self._pack_value(value, timeout)
            real_timeout = self._get_memcache_timeout(timeout +
                CACHE_HERD_TIMEOUT)
        else:
            packed = value
            real_timeout = self._get_memcache_timeout(timeout)
        return self._cache.add(self.make_key(key, version=version), packed, real_timeout)

    def get(self, key, default=None, version=None):
        encoded_key = self.make_key(key, version=version)
        packed = self._cache.get(encoded_key)
        if packed is None:
            return default
        
        val, refresh = self._unpack_value(packed)
        
        # If the cache has expired according to the embedded timeout, then
        # shove it back into the cache for a while, but act as if it was a
        # cache miss.
        if refresh:
            self._cache.set(encoded_key, val,
                self._get_memcache_timeout(CACHE_HERD_TIMEOUT))
            return default
        
        return val

    def set(self, key, value, timeout=None, version=None, herd=True):
        # If the user chooses to use the herd mechanism, then encode some
        # timestamp information into the object to be persisted into memcached
        if herd and timeout != 0:
            if timeout is None:
                timeout = self.default_timeout
            packed = self._pack_value(value, timeout)
            real_timeout = self._get_memcache_timeout(timeout +
                CACHE_HERD_TIMEOUT)
        else:
            packed = value
            real_timeout = self._get_memcache_timeout(timeout)
        return self._cache.set(self.make_key(key, version=version), packed, real_timeout)

    def delete(self, key, version=None):
        self._cache.delete(self.make_key(key, version=version))

    def get_many(self, keys, version=None):
        # First, map all of the keys through our key function
        rvals = map(lambda k: self.make_key(k, version=version), keys)
        
        packed_resp = self._cache.get_multi(rvals)
        
        resp = {}
        reinsert = {}
                
        for key, packed in packed_resp.iteritems():
            # If it was a miss, treat it as a miss to our response & continue
            if packed is None:
                resp[key] = packed
                continue
            
            val, refresh = self._unpack_value(packed)
            if refresh:
                reinsert[key] = val
                resp[key] = None
            else:
                resp[key] = val
        
        # If there are values to re-insert for a short period of time, then do
        # so now.
        if reinsert:
            self._cache.set_multi(reinsert,
                self._get_memcache_timeout(CACHE_HERD_TIMEOUT))
        
        # Build a reverse map of encoded keys to the original keys, so that
        # the returned dict's keys are what users expect (in that they match
        # what the user originally entered)
        reverse = dict(zip(rvals, keys))
        
        return dict(((reverse[k], v) for k, v in resp.iteritems()))

    def close(self, **kwargs):
        self._cache.disconnect_all()
    
    def set_many(self, data, timeout=None, version=None, herd=True):
        if herd and timeout != 0:
            safe_data = dict(((self.make_key(k, version=version), self._pack_value(v, timeout))
                for k, v in data.iteritems()))
        else:
            safe_data = dict((
                (self.make_key(k, version=version), v) for k, v in data.iteritems()))
        self._cache.set_multi(safe_data, self._get_memcache_timeout(timeout))
    
    def delete_many(self, keys, version=None):
        self._cache.delete_multi(map(lambda k: self.make_key(k, version=version), keys))
    
    def clear(self):
        self._cache.flush_all()

import functools

from google.appengine.api import memcache

_cache_keys = []

def cache(key):
    def wrapper(f):
        @functools.wraps(f)
        def g(*args, **kwargs):
            result = memcache.get(key)
            if result is None:
                result = f(*args, **kwargs)
                memcache.set(key, result)
            return result
        return g
    return wrapper

def flush_all():
    for k in _cache_keys:
        memcache.delete(k)

import functools

from google.appengine.api import memcache

_cache_keys = []

def cache(key):
    def wrapper(f):
        @functools.wraps
        def g(*args, **kwargs):
            result = memcache.get(key)
            if result is None:
                result = f(*args, **kwargs)
                memcache.set(key, result)
            return result
    return wrapper

def flush_all():
    for k in keys:
        memcache.delete(k)

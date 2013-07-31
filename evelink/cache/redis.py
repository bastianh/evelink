import logging

try:
    import cPickle as pickle
except:
    import pickle

from evelink import api

_log = logging.getLogger('evelink.cache')


class RedisCache(api.APICache):
    """An implementation of APICache using a redis connection."""

    def __init__(self, redis):
        super(RedisCache, self).__init__()
        self.connection = redis

    def get(self, key):
        result = self.connection.get(key)
        if not result:
            _log.info("api cache miss %r",key)
            return None
        _log.info("api cache hit %r",key)
        return pickle.loads(result)

    def put(self, key, value, duration):
        _log.info("put to cache %r for %r -> %r",key, duration, value)
        self.connection.setex(key,duration,pickle.dumps(value))

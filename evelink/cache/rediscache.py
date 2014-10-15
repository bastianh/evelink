from evelink.thirdparty.six.moves import cPickle as pickle
from evelink import api

class RedisCache(api.APICache):
    """An implementation of APICache using a redis.StrictRedis connection."""

    def __init__(self, strict_redis_connections):
        super(RedisCache, self).__init__()
        self.connection = strict_redis_connections

    def get(self, key):
        result = self.connection.get(key)
        if not result:
            return None
        return pickle.loads(result)

    def put(self, key, value, duration):
        self.connection.setex(key, duration, pickle.dumps(value))

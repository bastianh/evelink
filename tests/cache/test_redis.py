try:
    import redis
except ImportError:
    NO_REDIS = True
else:
    NO_REDIS = False

from tests.compat import unittest

from evelink.cache.rediscache import RedisCache

@unittest.skipIf(NO_REDIS, 'redis library not installed')
class RedisCacheTestCase(unittest.TestCase):

    def setUp(self):
        self.redis = redis.StrictRedis()
        self.cache = RedisCache(self.redis)

    def tearDown(self):
          pass

    def test_cache(self):
        self.cache.put('foo', 'bar', 3600)
        self.cache.put('bar', 1, 3600)
        self.cache.put('baz', True, 3600)
        self.assertEqual(self.cache.get('foo'), 'bar')
        self.assertEqual(self.cache.get('bar'), 1)
        self.assertEqual(self.cache.get('baz'), True)


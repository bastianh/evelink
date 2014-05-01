import time
from dogpile.cache.api import NoValue
import logging
try:
    import cPickle as pickle
except:
    import pickle

from evelink import api

logger = logging.getLogger("APICACHE")

class DogpileCache(api.APICache):
    """An implementation of APICache using a dogpile cache."""

    def __init__(self, region,cachetime_extension=0):
        super(DogpileCache, self).__init__()
        self.region = region
        self.cachetime_extension = cachetime_extension

    def get(self, key):
        result = self.region.get(key,ignore_expiration=True)
        if not result:
            logger.debug("NO RESULT %r %r",key,type(result))
            return None

        value,duration = pickle.loads(result)
        if duration+self.cachetime_extension > int(time.time()):
            logger.info("found cached item (duration: %r extra %d)",(duration - time.time())/60,self.cachetime_extension)
            return value
        logger.info("discarded cached item (duration: %r extra %d)",(duration - time.time())/60,self.cachetime_extension)
        return None

    def put(self, key, value, duration):
        logger.info("SAVING KEY %r FOR %r Sekunden",key,duration)
        if duration < 30:
            duration = 180
            logger.warn("Minimale Logtime auf %d Sekunden gesetzt!"%duration)
        self.region.set(key,pickle.dumps((value,duration+int(time.time()))))

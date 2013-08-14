# import our friend redis
import redis

# import our local stuffs
import local_settings


# ye olde database classe
class Database:
    def __init__(self):
        """
        Initalize all our lovely constants and stuff, and create a
        db connection object for later use.

        TODO:   move all this stuff to elsewhere: we don't want to need
                the local_settings files just to load this module, maybe?

        """
        # set the Redis constants
        self.redis_host = local_settings.REDIS_HOST
        self.redis_port = local_settings.REDIS_PORT
        self.redis_db = local_settings.REDIS_DB

        # connect to Redis
        self.db = self.get_redis_conn()

    def get_redis_conn(self):
        """
        Gets a connection to Redis, and returns the connection object.

        """
        redis_conn = redis.Redis(
            host=self.redis_host,
            port=self.redis_port,
            db=self.redis_db)

        return redis_conn

    def get(self, set_name, set_content):
        result = self.db.hget(set_name, set_content)
        return result

    def set(self, set_name, set_content):
        result = self.db.hmset(set_name, set_content)
        return result

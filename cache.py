# import the usual stuff
import time
import difflib
from datetime import datetime

# import our local stuffs
import local_settings
import database


# the cache class. 
class Cache:
    """
    Provides methods for fetching cached content and comparing its content
    against newly-fetched page content.

    """

    def __init__(self):
        """
        Initalize all our lovely constants and stuff, and create a 
        db connection object for later use.

        TODO:   move all this stuff to elsewhere: we don't want to need
                the local_settings files just to load this module

        """
        # set the redis constants
        self.redis_host = local_settings.REDIS_HOST
        self.redis_port = local_settings.REDIS_PORT
        self.redis_db = local_settings.REDIS_DB

        # create the Redis connection object
        db = database.Database()
        self.db = db.get_redis_conn()


    def fetch_cache(self):
        """
        Fetches the latest entry from the Redis cache

        """

        # greab the last-saved content out of the cache
        cached_content = self.db.hget('target_page_cache', 'page_content')

        return cached_content


    def diff_cache(self, target_content, cached_content):
        """
        Compare the newly-grabbed page content against the last cached version.

        """
        # if the cached content isn't empty (it can't compare against None)
        if cached_content is not None:
            # do a unified diff against the two sources
            diff = difflib.unified_diff(
                # splitlines is required, or else the output is a total mess
                cached_content.splitlines(1),
                target_content.splitlines(1)
            )

            # the output is a generator, so let's step through it to make
            # a string we can use later 
            diff_string = ""
            for line in diff:
                diff_string += line
        else:
            diff_string = None

        return diff_string


    def update_cache(self, target_content):
        """
        Update the page content stored in the cache.

        """
        unix_timestamp = int(time.mktime(datetime.now().timetuple()))
        cache_dict = {
            "page_content": target_content,
            "timestamp": unix_timestamp
        }
        cache_update = self.db.hmset('target_page_cache', cache_dict) 

        return cache_update


# if we're here to run, run it
if __name__ == "__main__":
    cache = Cache()
    cached_content = cache.fetch_cache()
    print cached_content

    # print(cache.update_cache(target_content))
    # print(cache.update_cache(''))
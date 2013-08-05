# import the usual stuff
import time
import difflib
from datetime import datetime

# import our favorite libraries
import requests
import redis
from bs4 import BeautifulSoup

# import our local stuffs
import local_settings


# the scraper class. the brains of the organization, really.
class Scraper:
    """
    Provides methods for scraping target pages and comparing their content
    against cached, earlier versions.

    TODO:   rename this class. and this file, probably.

    """

    def __init__(self):
        """
        Initalize all our lovely constants and stuff, and create a 
        db connection object for later use.

        TODO:   move all this stuff to elsewhere: we don't want to need
                the local_settings files just to load this module

        """
        # set the search parameter constants
        self.target_url = local_settings.TARGET_URL
        self.target_element_name = local_settings.TARGET_ELEMENT_NAME

        # set the redis constants
        self.redis_host = local_settings.REDIS_HOST
        self.redis_port = local_settings.REDIS_PORT
        self.redis_db = local_settings.REDIS_DB

        # create the Redis connection object
        self.db = self.get_redis_conn(
            self.redis_host,
            self.redis_port,
            self.redis_db
        )


    # fetch the page content
    def fetch_site_content(self, target_url, target_element_name='html'):
        """
        Fetches the content of the requested site, based on element types.
        It uses CSS selectors (jQuery-style), and defaults to `html`
        if not otherwise explicitly set. 
        
        """

        # snag the page content
        r = requests.get(target_url)
        soup = BeautifulSoup(r.text)

        # find all the divs matching the requested selectors
        target_html = soup.select(target_element_name)
        target_content = target_html[0].prettify(formatter="html")

        return target_content


    # grab the cached stuff out of Redis
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


    def get_redis_conn(self, redis_host, redis_port, redis_db):
        """
        Gets a connection to Redis, and returns the connection object.

        """
        redis_conn = redis.Redis(host=redis_host, port=redis_port, db=redis_db)

        return redis_conn



if __name__ == "__main__":

    scraper = Scraper()

    target_url = local_settings.TARGET_URL
    target_element_name = local_settings.TARGET_ELEMENT_NAME

    target_content = scraper.fetch_site_content(target_url, target_element_name)
    cached_content = scraper.fetch_cache()

    # print target_content
    # print cached_content

    diff = scraper.diff_cache(target_content, cached_content)
    if diff is not "":
        print 'There are some differences:'
        print diff
    else:
        print 'The target and cache match.'

    # print(scraper.update_cache(target_content))
    # print(scraper.update_cache('hi!'))

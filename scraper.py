# scrape at x interval
#   this might be easier to do with celery beat, actually
# 
# look for this word
#   requests
#       beautiful soup
# 
# if it's changed, do whatever
#   check against redis
#       if same, move on
#       if different, store, with timestamp
# 
# use difflib.unified_diff to calculate
# 
# Mandrill to send

# import the usual stuff
import time
from datetime import datetime

# import our favorite libraries
import requests
import redis
from bs4 import BeautifulSoup

# import our local stuffs
import local_settings


class Scraper:

    def __init__(self):
        # self.target_url = local_settings.TARGET_URL
        # self.target_element_name = local_settings.TARGET_ELEMENT_NAME

        self.redis_host = local_settings.REDIS_HOST
        self.redis_port = local_settings.REDIS_PORT
        self.redis_db = local_settings.REDIS_DB

        self.db = self.get_redis_conn(
            self.redis_host, self.redis_port, self.redis_db
        )


    # this is the primary bit
    def fetch_site_content(self, target_url, target_element_name='html'):
        """
        Fetches the content of the requested site, based on element types. It uses
        CSS selectors (jQuery-style), and defaults to `html` if not otherwise set. 
        
        """

        # snag the page content
        r = requests.get(target_url)
        soup = BeautifulSoup(r.text)

        # find all the divs matching the requested selectors
        target_content = soup.select(target_element_name)

        return target_content


    def fetch_cache(self):
        """
        Fetches the latest entry from the Redis cache

        """
        self.db.hgetall('target_page_cache')


    def diff_cache(self):
        """
        Compare against the last cached version

        """
        pass


    def update_cache(self, db, target_content):
        """


        """
        unix_timestamp = int(time.mktime(datetime.now().timetuple()))

        cache_dict = {
            "cache_content": target_content,
            "timestamp": unix_timestamp
        }

        cache_update = db.hmset('target_page_cache', cache_dict) 

        return cache_update


    def get_redis_conn(self, redis_host, redis_port, redis_db):
        """
        Gets a connection to Redis, and returns the connection object.

        """
        return redis.Redis(host=redis_host, port=redis_port, db=redis_db)



if __name__ == "__main__":

    scraper = Scraper()
    target_url = local_settings.TARGET_URL
    target_element_name = local_settings.TARGET_ELEMENT_NAME
    print scraper.fetch_site_content(target_url, target_element_name)

    # scraper.fetch_cache(db)
    # print scraper.update_cache(db)

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
import difflib
import sys
from datetime import datetime

# import our favorite libraries
import requests
import redis
from bs4 import BeautifulSoup

# import our local stuffs
import local_settings


class Scraper:
    """

    """

    def __init__(self):
        """
        Initalize all our lovely constants and stuff, and create a 
        db connection object for later use.

        """
        self.target_url = local_settings.TARGET_URL
        self.target_element_name = local_settings.TARGET_ELEMENT_NAME

        self.redis_host = local_settings.REDIS_HOST
        self.redis_port = local_settings.REDIS_PORT
        self.redis_db = local_settings.REDIS_DB

        # get your connection to Redis set
        self.db = self.get_redis_conn(
            self.redis_host,
            self.redis_port,
            self.redis_db
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
        target_html = soup.select(target_element_name)
        target_content = target_html[0].prettify().encode('UTF-8')

        # target_content = "".join(line.strip() for line in str(target_html).split("\n"))

        return target_content


    def fetch_cache(self):
        """
        Fetches the latest entry from the Redis cache

        """

        # greab the last-saved content out of the cache
        # cached_content = self.db.hgetall('target_page_cache')
        cached_content = self.db.hget('target_page_cache', 'page_content')

        return cached_content


    def diff_cache(self, target_content, cached_content):
        """
        Compare the newly-grabbed page content against the last cached version.

        """
        if cached_content is not None:
            print type(target_content)
            print '***'
            print type(cached_content)

            diff = difflib.unified_diff(
                        unicode(str(target_content), errors='ignore'),
                        unicode(str(cached_content), errors='ignore'))
            for line in diff:
                sys.stdout.write(line)
            # sys.stdout.writelines(diff)
        else:
            diff = None

        return diff


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
        return redis.Redis(host=redis_host, port=redis_port, db=redis_db)



if __name__ == "__main__":

    scraper = Scraper()

    target_url = local_settings.TARGET_URL
    target_element_name = local_settings.TARGET_ELEMENT_NAME

    target_content = scraper.fetch_site_content(target_url, target_element_name)
    cached_content = scraper.fetch_cache()

    print target_content
    print cached_content

    print(scraper.diff_cache(target_content, cached_content))

    # print(scraper.update_cache(target_content))
    print(scraper.update_cache('hi!'))

    # scraper.fetch_cache(db)
    # print scraper.update_cache(db)

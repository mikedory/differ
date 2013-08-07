# import our favorite libraries
import logging

# TODO: move the local settings stuff to here.
import local_settings

from scraper import Scraper
from cache import Cache


class App:
    def __init__(self):
        # fire up scraper and cache object
        self.scraper = Scraper()
        self.cache = Cache()


    def run_scraper(self, target_url, target_element_name):
        """
        Run the scraper, check the cache, and log the differences.

        """
        # define the target and cached content
        target_content = self.scraper.fetch_site_content(
            target_url,
            target_element_name
        )
        cached_content = self.cache.fetch_cache()

        # check the cache and report our findings
        if target_content is not None:
            diff = self.cache.diff_cache(target_content, cached_content)
            if diff is not "":
                logging.info('The target differs from the cache.')
                logging.info(diff)

                logging.info('Updating cache...')
                self.cache.update_cache(target_content)
                logging.info('Cache updated.')
            else:
                logging.info('The target and cache match. Not altering cache.')
        else:
            logging.warn('Unable to fetch requested page! D:')
            logging.error('Scraping falure.')

        return 'Scraping complete.'


if __name__ == '__main__':
    app = App()

    # define the target to hit
    target_url = local_settings.TARGET_URL
    target_element_name = local_settings.TARGET_ELEMENT_NAME

    # run scraper!
    scrape_result = app.run_scraper(target_url, target_element_name)
    print scrape_result
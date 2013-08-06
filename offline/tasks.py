import logging

from scraper import Scraper
from cache import Cache

from celery import Celery
import offline.celeryconfig

# define our tasks and config module
celery = Celery('tasks')
celery.config_from_object('offline.celeryconfig')


@celery.task
def scrape(target_url, target_element_name):
    """
    Create a task that Celery can run to scrape and update all the things.

    """
    # fire up scraper and cache object
    scraper = Scraper()
    cache = Cache()

    # debug, if desired
    logging.debug('Using config file %s' % offline.celeryconfig.__name__)

    # define the target and cached content
    target_content = scraper.fetch_site_content(target_url, target_element_name)
    cached_content = cache.fetch_cache()

    # check the cache and report our findings
    if target_content is not None:
        diff = cache.diff_cache(target_content, cached_content)
        if diff is not "":
            logging.info('The target differs from the cache.')
            logging.info(diff)

            logging.info('Updating cache...')
            scraper.update_cache(target_content)
            logging.info('Cache updated.')
        else:
            logging.info('The target and cache match. Not altering cache.')
    else:
        logging.warn('Unable to fetch requested page! D:')
        logging.error('Scraping falure.')

    return 'Scraping complete.'
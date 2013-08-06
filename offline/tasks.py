import logging

import local_settings
from scraper import Scraper

from celery import Celery
import offline.celeryconfig

logging.info('Firing up Celery with config file %s...' 
    % offline.celeryconfig.__name__)

celery = Celery('tasks')
celery.config_from_object('offline.celeryconfig')


@celery.task
def scrape():
    """
    Create a task that Celery can run to scrape and update all the things.

    """

    # fire up a scraper object
    scraper = Scraper()

    # define the target to hit
    target_url = local_settings.TARGET_URL
    target_element_name = local_settings.TARGET_ELEMENT_NAME

    target_content = scraper.fetch_site_content(target_url, target_element_name)
    cached_content = scraper.fetch_cache()

    # check the cache and report our findings
    if target_content is not None:
        diff = scraper.diff_cache(target_content, cached_content)
        message = ""
        if diff is not "":
            logging.info('There are some differences...')
            logging.info(diff)
            message = diff

            logging.info('Updating cache...')
            scraper.update_cache(target_content)
        else:
            logging.info('The target and cache match.')
            logging.info('Leaving cache alone.')
            message = None
    else:
        logging.info('Unable to fetch requested page! D:')
        logging.info('Connection falure.')
        message = None

    return message
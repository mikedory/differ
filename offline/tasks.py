# import our favorite libraries
import logging

# import our local stuffs
from app import App

from celery import Celery
import offline.celeryconfig

# define our tasks and config module
celery = Celery('tasks')
celery.config_from_object('offline.celeryconfig')


@celery.task
def scrape_and(target_url, target_element_name):
    """
    Create a task that Celery can run to scrape and update all the things.

    """
    # debug, if desired
    logging.debug('Running scraper task...')
    logging.debug('Using config file %s' % offline.celeryconfig.__name__)

    # fire up app, and run the scraper
    app = App()
    task_result = app.run_scraper(target_url, target_element_name)

    logging.debug('task complete!')

    return task_result
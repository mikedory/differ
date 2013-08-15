# import our favorite libraries
import logging

# TODO: move the local settings stuff to here.
import local_settings

# import our modules
from scraper import Scraper
from cache import Cache
from email import Email


class App:
    def run_scraper(self, target_url, target_element_name):
        """
        Run the scraper, check the cache, and log the differences.

        """

        # fire up scraper and cache object
        scraper = Scraper()
        cache = Cache()

        # define the target and cached content
        target_content = scraper.fetch_site_content(
            target_url,
            target_element_name
        )
        cached_content = cache.fetch_cache(target_url)

        # check the cache and report our findings
        if target_content is not None:
            diff = cache.diff_cache(target_content, cached_content)
            if diff is not u'':
                logging.info('The target differs from the cache.')
                logging.info(diff)

                logging.info('Updating cache...')
                cache.update_cache(target_url, target_content)
                logging.info('Cache updated.')
                message = 'Success! Cache updated.'
            else:
                logging.info('The target and cache match. Not altering cache.')
                message = 'Success! Cache not altered.'
        else:
            logging.warn('Unable to fetch requested page! D:')
            logging.error('Scraping falure.')
            message = 'Failure!'

        logging.info('Scraper finished.')

        return message, diff

    def send_email(self, diff):
        email = Email()

        html = '<h1>'

        email_attempt = email.send_email(
            html,
            subject,
            from_email,
            to_email,
            to_name
        )

        return email_attempt

if __name__ == '__main__':
    # if run directly, try running the scraper and printing the results
    app = App()

    # run scraper!
    for target_url, target_element in local_settings.TARGET_URLS:
        scrape_result, diff = app.run_scraper(target_url, target_element)
        print(scrape_result)
        print(diff)

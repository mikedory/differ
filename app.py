# import our favorite libraries
import logging
import cgi

# TODO: move the local settings stuff to here.
import config.local_settings as local_settings

# import our modules
from lib.scraper import Scraper
from lib.cache import Cache
from lib.email import Email


class App:
    def run_scraper(self, target_url, target_element_name):
        """
        Run the scraper, check the cache, and log the differences.

        """

        # fire up scraper and cache objects
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

                logging.info('Sending mail...')
                email_result = self.send_email(target_url, diff)
                logging.info(email_result)

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

    def send_email(self, target_url, diff):
        email = Email()

        # escape HTML characters in the diff
        diff = cgi.escape(diff)

        subject = 'Content update for %s' % target_url
        html = '<h1>Content update for %s</h1><pre>%s</pre>' % (target_url, diff)
        from_email = local_settings.EMAIL_FROM_ADDRESS
        to_email = local_settings.EMAIL_TO_ADDRESS
        to_name = local_settings.EMAIL_TO_NAME

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

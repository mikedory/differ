# import our favorite libraries
import requests
from bs4 import BeautifulSoup

# import our local stuffs
import local_settings


# the scraper class. the brains of the organization, really.
class Scraper:
    """
    Provides methods for scraping target pages and comparing their content
    against cached, earlier versions.

    """

    def fetch_site_content(self, target_url, target_element_name='html'):
        """
        Fetches the content of the requested site, based on element types.
        It uses CSS selectors (jQuery-style), and defaults to `html`
        if not otherwise explicitly set.

        """
        # snag the page content
        try:
            # attempt to request and parse the target content
            r = requests.get(target_url)
            soup = BeautifulSoup(r.text)

            # find all the divs matching the requested selectors
            target_html = soup.select(target_element_name)
            target_content = target_html[0].prettify(formatter="html")

        # if the request fails, return None
        except requests.exceptions.ConnectionError:
            target_content = None

        return target_content


# if we're here to run, run it
if __name__ == "__main__":
    """
    When run on its own, the scraper will go fetch the target content
    and print it out.

    """
    # initialize the scraper
    scraper = Scraper()

    # define yer targets
    target_url = local_settings.TARGET_URL
    target_element_name = local_settings.TARGET_ELEMENT_NAME

    # scrape stuff!
    target_content = scraper.fetch_site_content(target_url, target_element_name)

    print(target_content)

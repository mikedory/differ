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

# import our favorite libraries
import requests
from bs4 import BeautifulSoup

# import our local stuffs
import local_settings

# this is the primary bit
def fetch_site(
        target_url,
        target_element_name='html'
    ):
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


def fetch_cache():
    """
    Fetches the latest entry from the Redis cache

    """
    pass


def compare_cached():
    """
    Compare against the last cached version

    """
    pass


if __name__ == "__main__":
    target_url = local_settings.TARGET_URL
    target_element_name = local_settings.TARGET_ELEMENT_NAME

    print fetch_site(target_url, target_element_name)

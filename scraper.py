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
        target_element_type=None,
        target_element_name=None
    ):
    """
    Fetches the content of the requested site, based on element types 
    and names (both of which are optional). 
    
    """

    # snag the page content
    r = requests.get(target_url)
    soup = BeautifulSoup(r.text)

    # find all the divs matching the requested 
    target_content = soup.find(target_element_type, target_element_name)

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
    target_element_type = local_settings.TARGET_ELEMENT_TYPE
    target_element_name = local_settings.TARGET_ELEMENT_NAME

    print fetch_site(target_url, target_element_type, target_element_name)

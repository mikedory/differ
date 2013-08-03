# scrape at x interval
#   this might be easier to do with celery beat, actually

# look for this word
#   requests
#       beautiful soup

# if it's changed, do whatever
#   check against redis
#       if same, move on
#       if different, store, with timestamp


def main():
    print "hi!"

if __name__ == "__main__":
    main()
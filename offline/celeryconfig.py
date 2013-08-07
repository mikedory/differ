# import the usual stuff
from datetime import timedelta

# import our local stuffs
import local_settings


""" 
Set up the backend defaults for the results and broker
(based heavily on: https://gist.github.com/vivekn/1062526)

TODO:   move this stuff into local_settings

"""

BROKER_URL = '%s://%s:%d/%d' % (
    local_settings.BROKER_BACKEND,
    local_settings.BROKER_HOST,
    local_settings.BROKER_PORT,
    local_settings.BROKER_DB
)

CELERY_IMPORTS = ("offline.tasks", ) # Module which contains the tasks you want to call asynchronously


"""
Set up the scheduler, which will then tell celery beat how often to run, and
what command to run when invoked.

Start the worker:

    celery -A offline.tasks worker --config=offline.celeryconfig --loglevel=info

Start the scheduler:

    celery beat --config="offline.celeryconfig" \
        --loglevel="info" --schedule="/tmp/celerybeat_schedule.db"

Rather than running workers and the `beat` task, run a single worker in beat mode:

    celery -A offline.tasks worker --config=offline.celeryconfig --loglevel=info -B

"""

# define the target to hit
target_url = local_settings.TARGET_URL
target_element_name = local_settings.TARGET_ELEMENT_NAME

# schedulize it
CELERYBEAT_SCHEDULE = {
    'scrape-site': {
        'task': 'offline.tasks.scrape_and_diff',
        'schedule': timedelta(seconds=10),
        'args': (target_url, target_element_name)
    },
}

# timezone (UTC ALL THE THINGS!)
CELERY_TIMEZONE = 'UTC'

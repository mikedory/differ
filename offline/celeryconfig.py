# from datetime import timedelta

import local_settings

""" 
set up the backend defaults for the results and broker

based heavily on: https://gist.github.com/vivekn/1062526

TODO:   move this stuff into local_settings

"""

BROKER_URL = '%s://%s:%d/%d' % (
    local_settings.BROKER_BACKEND,
    local_settings.BROKER_HOST,
    local_settings.BROKER_PORT,
    local_settings.BROKER_DB
)

# CELERY_IMPORTS = ("module.submodule.foo", ) # Module which contains the tasks you want to call asynchronously


"""
set up the scheduler

"""


# CELERYBEAT_SCHEDULE = {
#     'add-every-30-seconds': {
#         'task': 'tasks.add',
#         'schedule': timedelta(seconds=30),
#         'args': (16, 16)
#     },
# }

# CELERY_TIMEZONE = 'UTC'

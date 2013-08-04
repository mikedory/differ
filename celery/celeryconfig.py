from datetime import timedelta

''' 
set up the backend defaults for the results and broker

based heavily on: https://gist.github.com/vivekn/1062526
'''

CELERY_RESULT_BACKEND = "redis"
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0
 
BROKER_BACKEND = "redis"
BROKER_HOST = "localhost"  # Maps to redis host.
BROKER_PORT = 6379         # Maps to redis port.
BROKER_VHOST = "0"         # Maps to database number.
 
CELERY_IMPORTS = ("module.submodule.foo", ) # Module which contains the tasks you want to call asynchronously


'''
set up the scheduler
'''


CELERYBEAT_SCHEDULE = {
    'add-every-30-seconds': {
        'task': 'tasks.add',
        'schedule': timedelta(seconds=30),
        'args': (16, 16)
    },
}

CELERY_TIMEZONE = 'UTC'

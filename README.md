Schedulizer
===========

Check a web page for a specific element, and run a diff on it.  If it's changed from the last check, send an email with the diff!


Requirements
------------

- Python 2.7+
- Redis
- Celery
- Requests
- Beautiful Soup
- Supervisor

You'll need a place to host this, a Mandrill account, and a webpage (or any HTML document) that you want to monitor.


Usage
-----

### Celery

Start the worker:

    celery -A offline.tasks worker --config=offline.celeryconfig --loglevel=info

Start the scheduler:

    celery beat --config="offline.celeryconfig" --loglevel="info" --schedule="/tmp/celerybeat_schedule.db"

Or optionally, run a single worker in beat mode (if you know this will only ever be one worker), and then you don't need the scheduler:

    celery -A offline.tasks worker --config=offline.celeryconfig --loglevel=info -B


TODO
----

Err, make this work.


Changelog
---------

First release! Woot!


License
-------

Basically, totally open.  Go to town.
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

#### Worker/Beat

Start the worker:

    celery -A offline.tasks worker --config=offline.celeryconfig --loglevel=info

Start the scheduler:

    celery beat --config="offline.celeryconfig" --loglevel="info" --schedule="/tmp/celerybeat_schedule.db"

And as with all background processes, you'll probably want to [daemonize Celery](http://docs.celeryproject.org/en/master/tutorials/daemonizing.html), and then run it via [Supervisord](https://github.com/celery/celery/tree/master/extra/supervisord) (or init.d, launchd, etc.).


#### Single-worker

Rather than running workers and the `beat` task, run a single worker in beat mode (if you know this will only ever be one worker — especially handy for running on services like Heroku).  This way, you can run everything with one command:

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
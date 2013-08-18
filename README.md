Differ
======

Differ is a Python-based tool that will check specified web pages at specified intervals, and email the user the differences between checks (if any are found).


Requirements
------------

- Python 2.7+
- Redis
- Celery
- Requests
- Beautiful Soup
- Supervisor

You'll also need a place to host this (and/or a Heroku account), a Mandrill account, and a webpage (or any HTML document) that you want to monitor.


Usage
-----

You can run this app in one of two ways: as a stand-alone command (handy to do manual site diffs or join up with a Cron task or Herou's Scheduler), or as a scheduled process via Celery.

### Stand-alone

First off, you're doing this in a virtual environment, right?  So make sure you've set that up properly:

    virtualenv differ-venv --distribute
    source ./differ-venv/bin/activate

Then install your dependancies:

    pip install -r requirements.txt

Run the full task thusly:

    python app.py

The output from this task will go to stdout, and if an email is specified, the differences will be emailed!


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

- Better document email functionality.
- Create example using MongoDB (or Postgres) in addition to Redis.
- Add a web panel for adding further scraping targets.


Changelog
---------

First release! Woot!


About
-----

This project was developed by [Mike Dory](https://github.com/mikedory).  Pull requests are welcome, as are bugs, feature requests, and general suggestions, so fire away. =)

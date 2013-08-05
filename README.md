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

Celery

    celery -A offline.tasks worker --config=offline.celeryconfig


TODO
----

Err, make this work.


Changelog
---------

First release! Woot!


License
-------

Basically, totally open.  Go to town.
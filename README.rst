=======
hivi.mx
=======


Collaborative live playlist using dailymotion API.

TODO
----

- use oembed
- use socketio/wamp/pythonium


Install'n run
=============

::

  pip install django django-socketio-alt memo memo-client
  git clone git://github.com/amirouche/hivi.mx.git

Then run the following::

  ./hivimx/manage.py runserver_socketio
  ./hivimx/front/stations.py
  ./hivimx/manage.py runserver 0.0.0.0:8001

Then go to `http://0.0.0.0:8001/ <http://0.0.0.0:8001/>`_

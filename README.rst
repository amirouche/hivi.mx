=======
hivi.mx
=======


Collaborative live playlist only dailymotion is supported yet.


Install'n run
=============

::

  pip install django memo git+git@github.com:amirouche/dailymotion-sdk-python-unofficial.git

Then run the following::

  ./hivimx/manage.py runserver_socketio
  ./hivimx/front/stations.py
  ./hivimx/manage.py runserver 0.0.0.0:8001

Then go to `http://0.0.0.0:8001/ <http://0.0.0.0:8001/>`_

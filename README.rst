django-feedmapper
=================

django-feedmapper is a library for synchronizing data from feeds with Django models. The process of synchronizing the data requires the use of three pieces: a parser, a mapping, and a schedule.

Example project
***************

Clone this git repo::

    git clone git@github.com:natgeo/django-feedmapper.git
    cd django-feedmapper

Make sure you have `virtualenvwrapper`_ installed and create a virtual environment::

    mkvirtualenv --no-site-packages --distribute django-feedmapper
    workon django-feedmapper

.. _virtualenvwrapper: http://www.doughellmann.com/docs/virtualenvwrapper/

Install the requirements::

    pip install -r requirements.txt

Synchronize the database and load the dummy data::

    cd example
    ./manage.py syncdb

Synchronize the dummy data::

    ./manage.py feedmapper_sync

Fire up the development server::

    ./manage.py runserver

Check out the feed mapping in the admin at http://localhost:8000/admin/feedmapper/mapping/1/
and the sync results in the admin at http://localhost:8000/admin/myapp/thing/.

Full documentation
******************

Documentation is on Read the Docs: http://readthedocs.org/docs/django-feedmapper/.


django-feedmapper
=================

django-feedmapper is a library for synchronizing data from feeds with Django models. The process of synchronizing the data requires the use of three pieces: a parser, a mapping, and a schedule.

Example project
***************

Clone this git repo::

    git clone git@github.com:natgeo/django-feedmapper.git
    cd django-feedmapper/example/

Make sure you have `virtualenvwrapper`_ installed and create a virtual environment::

    mkvirtualenv --no-site-packages --distribute django-feedmapper
    workon django-feedmapper

.. _virtualenvwrapper: http://www.doughellmann.com/docs/virtualenvwrapper/

Install the requirements::
    
    pip install -r requirements.txt

Synchronize the database::

    ./manage.py syncdb

Load up some dummy data::

    ./manage.py loaddata dev_data.json

Synchronize the dummy data::

    ./manage.py feedmapper_sync

Fire up the development server::

    ./manage.py runserver

Check out the sync results in the admin at http://localhost:8000/admin/myapp/thing/.

Full documentation
******************

The full documentation is in the ``docs`` folder. You'll need to have Sphinx installed to build the documentation::

    pip install Sphinx

Building the documentation is easy::

    cd django-feedmapper/docs/
    make html
    open build/html/index.html

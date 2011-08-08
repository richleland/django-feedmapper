django-feedmapper
=================

django-feedmapper is a library for synchronizing data from feeds with Django models. The process of synchronizing the data requires the use of three pieces: a parser, a mapping, and a schedule.

Parsers
*******

A parser defines methods for validating and parsing data from incoming feeds. There are two built-in parsers, :py:class:`~feedmapper.parsers.XMLParser` and :py:class:`~feedmapper.parsers.AtomParser`. You can write your own parser by subclassing the base :py:class:`~feedmapper.parsers.Parser` class.

Mapping
*******

A mapping is written in JSON and describes how and when data from an incoming feed should be mapped to Django models. You can perform the following types of mappings:

* One field in a model to one field from a feed
* One field in a model to multiple fields from a feed
* One field in a model to a transformer method on the model

You can also set the following properties on a mapping through the Django admin:

* Data source
* Synchronization schedule
* Purge existing data

An example: users
-----------------

Let's get into an example. Suppose we have the following incoming XML data and we want to map each ``<user>`` to Django's ``User`` model:

.. code-block:: xml
   :linenos:

    <?xml version="1.0" ?>
    <auth>
        <users>
            <user>
                <username>vader</username>
                <first_name>Anakin</first_name>
                <last_name>Skywalker</last_name>
                <email>vader@sith.org</email>
                <date_joined>2050-01-31T20:00-4:00</date_joined>
            </user>
            <user>
                <username>kenobi</username>
                <first_name>Obi-Wan</first_name>
                <last_name>Kenobi</last_name>
                <email>kenobi@jedi.org</email>
                <date_joined>2000-01-31T20:00-4:00</date_joined>
            </user>
        </users>
    </auth>

We need to specify a JSON map:

.. code-block:: javascript
   :linenos:

    {
      "models": {
        "myapp.Thing": {
          "nodePath": "users.user",
          "identifier": "username",
          "fields": {
            "username": "username",
            "email": "email",
            "name": ["first_name", "last_name"],
            "date_joined": {
              "transformer": "convert_date",
              "fields": ["date_joined"]
            }, 
          } 
        }
      }
    }

Let's break this down a bit. First, we can specify one or more models to map:

.. code-block:: javascript
   :linenos:

      "models": {
        "myapp.Thing": {

We need to tell the parser the path to all of the ``<user>`` elements:

.. code-block:: javascript
   :linenos:

          "nodePath": "users.user",

If the mapping has purging turned off, we need to supply a unique idenfier for Django ORM ``get`` calls. In this case our resulting ORM call would be ``User.objects.get(username=username)``:

.. code-block:: javascript
   :linenos:

          "identifier": "username",

Now the fun part. Mapping the fields:

.. code-block:: javascript
   :linenos:

          "fields": {
            "username": "username",
            "email": "email",
            "name": ["first_name", "last_name"],
            "date_joined": {
              "transformer": "convert_date",
              "fields": ["date_joined"]
            }, 
          } 

We've got example of all three types of field mappings here.

``username`` and ``email`` are one-to-one mappings:

.. code-block:: javascript
   :linenos:

            "username": "username",
            "email": "email",

``name`` is mapped to multiple fields. The parser will concatenate these fields, putting a space between them:

.. code-block:: javascript
   :linenos:

            "name": ["first_name", "last_name"],

``date_joined`` uses a transformer, which is simply a method defined on your model to do some manipulation to the incoming data before inserting it in a field. Here we tell the parser that the ``date_joined`` field should map to the ``date_joined`` field in the XML but use the ``convert_date`` method to transform the incoming data:

.. code-block:: javascript
   :linenos:

            "date_joined": {
              "transformer": "convert_date",
              "fields": ["date_joined"]
            }, 

Scheduling
**********

.. note:: DEV IS STILL IN PROGRESS FOR THIS. IT WILL CHANGE.

Mappings define when and what should be updated. The execution should be handled by `celery`_ workers. We need to have a way to create scheduled tasks dynamically. The `django-celery`_ library handles this using `custom scheduler classes`_.

We may want to consider creating management commands to handle the synchronization as well that can be set up as cron jobs.

.. _celery: http://celeryproject.org/
.. _django-celery: http://packages.python.org/django-celery/
.. _custom scheduler classes: http://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html#using-custom-scheduler-classes

Contents
********

.. toctree::
   :maxdepth: 2
   :glob:

   *

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


django-feedmapper
=================

django-feedmapper is a library for synchronizing data from feeds with Django models.

Existing solutions in the same vain
***********************************

* http://www.feedjack.org/
* https://github.com/tabo/feedjack
* https://github.com/matagus/django-planet

Feed types supported
********************

* `Atom`_
* `NITF`_
* `Prism`_
* `RSS`_

.. _Atom: http://en.wikipedia.org/wiki/Atom_(standard)
.. _NITF: http://www.iptc.org/site/News_Exchange_Formats/NITF/
.. _Prism: http://www.idealliance.org/specifications/prism/
.. _RSS: http://en.wikipedia.org/wiki/Rss

Parsers
*******

.. note:: describe how to create a parser subclass

Parsers should:

* Subclass the base Parser class
* Use `lxml`_ to traverse XML feeds
* Define the xpath to a collection of items within the feed
* Provide methods for parsing a mapping
* Store the parsed raw XML and, if it has not changed, do nothing (bad idea?)
* Handle translation of feed data type to model data type (e.g. date)

.. _lxml: http://lxml.de/

Mapping
*******

.. note:: describe how to map a feed to a model

Mappings should:

* Have a field that points to a model
* Have a field that stores the url of a feed
* Have a field that stores the type of feed (which is really the parser)
* Have a field that stores a JSON representation of the mapping
* Create or update a scheduled task on save

A user should be able to:

* Map one field from a feed to one field from a model
* Map multiple fields from a feed to one field from a model
* Schedule in a cron-like style when feed parsing should occur
* Denote whether the scheduled parsing should update or overwrite existing objects

Questions to be answered:

* How do we map one field from a feed to one field from a model?
* How do we map many fields from a feed to one field from a model? (map to method?)
* How do we handle mapping to a model that has inlines/relationships? (e.g. shows with air datetimes)

Execution of updates
********************

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


django-feedmapper
=================

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
* Use `lxml`_ to traverse feeds
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


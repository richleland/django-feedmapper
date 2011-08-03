django-feedmapper
=================

django-feedmapper is a library for synchronizing data from feeds with Django models.

Parsers
*******

.. note:: describe how to create a parser subclass

Parsers should:

* Subclass the base Parser class
* Use `lxml`_ to traverse XML feeds
* Define the xpath to a collection of items within the feed
* Provide methods for parsing a mapping
* Handle translation of feed data type to model data type (e.g. date)

.. _lxml: http://lxml.de/

Mapping
*******

.. note:: describe how to map a feed to a model

Mappings should:

* Have a field that stores the url of a feed
* Have a field that stores the type of feed (which is really the parser)
* Have a field that stores a JSON representation of the mapping
* Create or update a scheduled task on save
* Store the parsed data and, if it has not changed, do nothing (hashed? raw?)

A user should be able to:

* Map one field from a feed to one field from a model
* Map multiple fields from a feed to one field from a model
* Schedule in a cron-like style when feed parsing should occur
* Denote whether the scheduled parsing should update or overwrite existing objects

Questions to be answered:

* How do we map one field from a feed to one field from a model?
* How do we map many fields from a feed to one field from a model? (map to method?)
* How do we handle mapping to a model that has inlines/relationships? (e.g. shows with air datetimes)

The core of the mapping lies in specifying a JSON map:

.. code-block:: javascript

    {
      "models": {
        "myapp.ShowTime": {
          "fields": {
            "date": {
              "fields": [
                "series.episode.showTime"
              ], 
              "transformer": "convert_date"
            }, 
            "premiere_type": "series.episode.showTime[@premiere_type]", 
            "episode": "FK! HOW TO OBTAIN EPISODE"
          }, 
          "identifier": "NEEDS UNIQUE IDENTIFIER"
        }, 
        "myapp.Episode": {
          "nodePath": "series.episode", 
          "identifier": "code", 
          "fields": {
            "code": "code", 
            "description": "description", 
            "show": "FK! HOW TO OBTAIN SHOW", 
            "final_title": "final_title", 
            "duration": "duration", 
            "title": "title", 
            "episode_title": "episode_title", 
            "theme": "theme", 
            "description_oneline": "description_oneline", 
            "webpub_leadtime": "webpub_leadtime", 
            "traffic_package": "traffic_package", 
            "vchip_rating": "vchip_rating", 
            "traffic_episode": "traffic_episode", 
            "geocore": "geocore"
          }
        }, 
        "myapp.Show": {
          "fields": {
            "description": "series.description", 
            "title": "series.title"
          }, 
          "identifier": "NEEDS UNIQUE IDENTIFIER"
        }
      }
    }


Execution of updates
********************

Mappings define when and what should be updated. The execution should be handled by `celery`_ workers. We need to have a way to create scheduled tasks dynamically. The `django-celery`_ library handles this using `custom scheduler classes`_.

We may want to consider creating management commands to handle the synchronization as well that can be set up as cron jobs.

.. _celery: http://celeryproject.org/
.. _django-celery: http://packages.python.org/django-celery/
.. _custom scheduler classes: http://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html#using-custom-scheduler-classes

Existing solutions in the same vain
***********************************

* http://www.feedjack.org/
* https://github.com/tabo/feedjack
* https://github.com/matagus/django-planet

Feed types of interest
**********************

* `Atom`_
* `NITF`_
* `Prism`_
* `RSS`_

.. _Atom: http://en.wikipedia.org/wiki/Atom_(standard)
.. _NITF: http://www.iptc.org/site/News_Exchange_Formats/NITF/
.. _Prism: http://www.idealliance.org/specifications/prism/
.. _RSS: http://en.wikipedia.org/wiki/Rss

NGC feeds
*********

.. note:: remove this before finalizing application

The XML from the NGC feed looks like the following:

.. code-block:: xml

    <?xml version="1.0" ?>
    <channel_guide>
        <series>
            <title><![CDATA[	World's Toughest Prisons	]]></title>
            <description><![CDATA[	No description available	]]></description>
            <episode>
                <code>276425</code>
                <title><![CDATA[	World's Toughest Prisons [TV-14 LSV]	]]></title>
                <final_title><![CDATA[	World's Toughest Prisons	]]></final_title>
                <episode_title><![CDATA[	World's Toughest Prisons	]]></episode_title>
                <vchip_rating><![CDATA[	TV-14 LSV	]]></vchip_rating>
                <traffic_package>NISD</traffic_package>
                <traffic_episode>3144</traffic_episode>
                <description_oneline><![CDATA[	Go behind the bars of two of the worlds toughest prisons, including one run by the inmates.	]]></description_oneline>
                <description><![CDATA[	NGC goes behind bars to see how inmates at two of the World's Toughest Prisons, Santa Martha in Mexico and Lurigancho in Peru, survive amid chaos, corruption and power struggles.  In Santa Martha, meet two former L.A. gang members who've formed an unlikely alliance to protect themselves. Then, at Lurigancho, authorities have handed over power to a council of inmate leaders. Meet two of these leaders, including a former head of a gang, and see how they maintain the fragile peace.	]]></description>
                <duration>60M</duration>
                <theme><![CDATA[	People & Places	]]></theme>
                <geocore><![CDATA[	Science & Space	]]></geocore>
                <webpub_leadtime>40</webpub_leadtime>
                <showTime premiere_type="">2011-07-31T20:00-4:00</showTime>
                <showTime premiere_type="">2011-07-31T23:00-4:00</showTime>
                <showTime premiere_type="">2011-08-07T10:00-4:00</showTime>
            </episode>
        </series>
    </channel_guide>

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


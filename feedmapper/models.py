from django.db import models
from django.utils.translation import ugettext_lazy as _

import jsonfield


PARSER_CHOICES = (
    ('feedmapper.parsers.XMLParser', 'XML'),
)

class Mapping(models.Model):
    "Represents a mapping of model fields to feed nodes or attributes."
    label = models.CharField(_("label"), max_length=255, help_text=_("Label for your reference"))
    source = models.URLField(_("source"), verify_exists=False, help_text=_("The source feed for your data"))
    parser = models.CharField(_("parser"), max_length=255, choices=PARSER_CHOICES, help_text=_("Which parser to use when synchronizing"))
    purge = models.BooleanField(_("purge"), default=False, help_text=_("Purge existing items on sync?"))
    data_map = jsonfield.JSONField(_("data map"))
    # to add: schedule for synchronization, notification emails?

    def __unicode__(self):
        return self.label

    def parse(self):
        "Dynamically pull in this mapping's parser and parse the mapping."
        module_path, parser_class = self.parser.rsplit('.', 1)
        module = __import__(module_path, fromlist=[parser_class])
        parser_class = getattr(module, parser_class)
        parser = parser_class(self)
        parser.parse()

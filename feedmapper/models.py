from django.db import models
from django.utils.translation import ugettext_lazy as _

import jsonfield


PARSER_CHOICES = (
    ('someapp.AtomParser', 'Atom'),
    ('someapp.RSSParser', 'RSS'),
)

class Mapping(models.Model):
    "Represents a mapping of model fields to feed nodes or attributes."
    label = models.CharField(_("label"), max_length=255, help_text=_("Label for your reference"))
    data_url = models.URLField(_("feed url"), verify_exists=False, help_text=_("The source feed for your data"))
    parser = models.CharField(_("parser"), max_length=255, choices=PARSER_CHOICES, help_text=_("Which parser to use when synchronizing"))
    overwrite = models.BooleanField(_("overwrite"), default=False, help_text=_("Overwrite items on sync?"))
    data_map = jsonfield.JSONField(_("data map"))
    # to add: schedule for synchronization, notification emails?

    def __unicode__(self):
        return self.label

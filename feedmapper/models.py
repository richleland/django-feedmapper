from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .fields import JSONField
from .settings import FEEDMAPPER


class Mapping(models.Model):
    "Represents a mapping of model fields to feed nodes or attributes."
    label = models.CharField(_("label"), max_length=255, help_text=_("Label for your reference"))
    source = models.URLField(_("source"), verify_exists=False, help_text=_("The source feed for your data"))
    parser = models.CharField(_("parser"), max_length=255, choices=FEEDMAPPER['PARSER_CHOICES'], help_text=_("Which parser to use when synchronizing"))
    purge = models.BooleanField(_("purge"), default=False, help_text=_("Purge existing items on sync?"))
    data_map = JSONField(_("data map"))
    notification_recipients = models.TextField(_("notification recipients"), blank=True, help_text=_("Specify one email address per line to be notified of parsing errors."))
    parse_attempted = models.DateTimeField(_("parse attempted"), blank=True, null=True)
    parse_succeeded = models.BooleanField(_("parse succeeded"))
    parse_log = models.TextField(_("parse log"), blank=True)

    def __unicode__(self):
        return self.label

    def parse(self):
        "Dynamically pull in this mapping's parser and parse the mapping."
        module_path, parser_class = self.parser.rsplit('.', 1)
        module = __import__(module_path, fromlist=[parser_class])
        parser_class = getattr(module, parser_class)
        parser = parser_class(self)
        parser.parse()

    if 'djcelery' in settings.INSTALLED_APPS:
        def save(self, *args, **kwargs):
            "Create or update a django-celery periodic task for this mapping."
            super(Mapping, self).save(*args, **kwargs)
            from djcelery.models import CrontabSchedule, PeriodicTask
            crontab, created = CrontabSchedule.objects.get_or_create(minute='0', hour='*', day_of_week='*')
            task = 'feedmapper.tasks.feedmapper_sync'
            args = '[%s]' % self.id
            task, created = PeriodicTask.objects.get_or_create(task=task, args=args)
            task.name = self.label
            if not (task.interval or task.crontab):
                task.crontab = crontab
            task.save()

from celery.task import task

from .models import Mapping


@task
def feedmapper_sync(mapping_id):
    "Grab the requested Mapping and parse it."
    try:
        mapping = Mapping.objects.get(pk=mapping_id)
        mapping.parse()
    except Mapping.DoesNotExist:
        logger = feedmapper_sync.get_logger()
        logger.info("feedmapper_sync failed for mapping with ID %s" % mapping_id)

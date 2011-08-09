from django.core.management.base import BaseCommand

from feedmapper.models import Mapping


class Command(BaseCommand):
    args = '<mapping_id mapping_id ...>'
    help = 'Synchronizes the specified mappings with their data sources.'

    def handle(self, *args, **options):
        mappings = Mapping.objects.all()
        if args:
            mappings = mappings.filter(id__in=args)
        if mappings:
            for mapping in mappings:
                mapping.parse()
        else:
            self.stdout.write("No mappings to parse.\n")

from django.conf import settings


FEEDMAPPER = {
    'DATA_DIR': '',
    'PARSER_CHOICES': (
        ('feedmapper.parsers.AtomParser', 'Atom'),
        ('feedmapper.parsers.XMLParser', 'XML'),
    ),
}

if hasattr(settings, 'FEEDMAPPER'):
    FEEDMAPPER.update(settings.FEEDMAPPER)

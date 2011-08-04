from lxml import etree
from StringIO import StringIO

from django.db.models import get_model


XML_DUMMY = """<?xml version="1.0" ?>
<auth>
    <users>
        <user>
            <id>2</id>
            <username>richleland</username>
            <first_name>Rich</first_name>
            <last_name>Leland</last_name>
            <email>rleland@ngs.org</email>
        </user>
        <user>
            <id>3</id>
            <username>jtk</username>
            <first_name>Captain</first_name>
            <last_name>Kirk</last_name>
            <email>jkirk@enterprise.org</email>
        </user>
    </users>
    <groups>
        <group>
            <id>2</id>
            <name>Cool people</name>
        </group>
    </groups>
</auth>
"""

class Parser(object):
    "Base paarser class for mapping Django model fields to feed nodes."
    def __init__(self, mapping):
        self.mapping = mapping

    def validate_model_format(self, model_string):
        "Validate that a model in the JSON mapping are in the format app.model."
        if not '.' in model_string or model_string.count('.') > 1:
            return False
        return True

    def parse(self):
        raise NotImplementedError("You must override the parse method in a Parser subclass.")


class XMLParser(Parser):
    "A parser for XML that does not follow any standard."

    def parse(self):
        """
        PSEUDOCODE
        for model in models:
            instance = model()
            field_mappings = model['fields'] # dict
            for model_field, mapped_to in field_mappings.items():
                instance[model_field] = mapped_to # lots of magic in mapped_to
            instance.save()
        """
        # this will change to etree.parse(mapping.data_url)
        tree = etree.parse(StringIO(XML_DUMMY))
        root = tree.getroot()

        model_mappings = self.mapping.data_map['models']
        for model_string, configuration in model_mappings.items():
            if not self.validate_model_format(model_string):
                raise ValueError("Invalid model format in JSON mapping: %s" % model_string)
            model = get_model(*model_string.split('.'))
            identifier = configuration.get('identifier')
            node_path = configuration['nodePath'].replace('.', '/')
            fields = configuration['fields']
            nodes = root.xpath(node_path)
            for node in nodes:
                instance = model()
                for field, target in fields.items():
                    if field != identifier:
                        if isinstance(target, basestring):
                            value = node.find(target).text
                            print "%s is mapped to one field: %s" % (field, value)
                        elif isinstance(target, list):
                            print "%s is mapped to many fields" % field
                        elif isinstance(target, dict):
                            transformer = getattr(instance, target['transformer'])
                            text_list = [node.find(field).text for field in target['fields']]
                            value = transformer(*text_list)
                            print value
                            print "%s is mapped using a transformer" % field
                        setattr(instance, field, value)
                instance.save()


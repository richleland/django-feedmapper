from lxml import etree

from django.db.models import get_model


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

    def join_fields(self, node, fields):
        "Joins the text for the specified fields."
        values = [node.find(field).text for field in fields]
        return " ".join(values)

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
        tree = etree.parse(self.mapping.source)
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
                            # maps one model field to one feed node
                            value = node.find(target).text
                        elif isinstance(target, list):
                            # maps one model field to multiple feed nodes
                            value = self.join_fields(node, target)
                        elif isinstance(target, dict):
                            # maps one model field to a transformer method
                            transformer = getattr(instance, target['transformer'])
                            text_list = [node.find(field).text for field in target['fields']]
                            value = transformer(*text_list)
                        setattr(instance, field, value)
                instance.save()


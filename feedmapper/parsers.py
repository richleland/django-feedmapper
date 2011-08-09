from lxml import etree

from django.db.models import get_model


class Parser(object):
    "Base parser class for mapping Django model fields to feed nodes."

    def __init__(self, mapping):
        self.mapping = mapping
        self.nsmap = {}

    def validate_model_format(self, model_string):
        "Validate that a model in the JSON mapping is in the format app.model."
        if not '.' in model_string or model_string.count('.') > 1:
            return False
        return True

    def parse(self):
        raise NotImplementedError("You must override the parse method in a Parser subclass.")


class XMLParser(Parser):
    "A parser for XML that does not follow any standard."

    def get_value(self, node, path):
        "Attempts to retrieve either the node text or node attribute specified."
        if '@' in path:
            if path.count('@') > 1:
                raise ValueError("You have more than one attribute accessor. (e.g. foo.@bar.@baz)")
            path, attr = path.rsplit('.@')
            resolved = node.find(path, namespaces=self.nsmap).attrib.get(attr, "")
        else:
            resolved = node.find(path, namespaces=self.nsmap).text
        return resolved

    def join_fields(self, node, fields):
        "Joins the text for the specified fields."
        values = [self.get_value(node, field) for field in fields]
        return " ".join(values)

    def parse(self):
        """
        Traverses through the XML document and parses the data, applying it to the
        model specified in the :py:class:`~feedmapper.models.Mapping`.
        """
        tree = etree.parse(self.mapping.source)
        root = tree.getroot()

        model_mappings = self.mapping.data_map['models']
        for model_string, configuration in model_mappings.items():
            if not self.validate_model_format(model_string):
                raise ValueError("Invalid model format in JSON mapping: %s" % model_string)
            identifier = configuration.get('identifier')
            if not identifier and not self.mapping.purge:
                raise UserWarning("Purging is off and the JSON mapping doesn't supply an identifier.")
            model = get_model(*model_string.split('.'))
            node_path = configuration['nodePath'].replace('.', '/')
            fields = configuration['fields']
            nodes = root.xpath(node_path, namespaces=self.nsmap)

            if self.mapping.purge:
                # remove existing items
                model.objects.all().delete()

            for node in nodes:
                if self.mapping.purge:
                    instance = model()
                else:
                    # purge is turned off, retrieve an existing instance
                    identifier_value = node.find(identifier, namespaces=self.nsmap).text
                    try:
                        instance = model.objects.get(pk=identifier_value)
                    except model.DoesNotExist:
                        instance = model()
                for field, target in fields.items():
                    if field != identifier:
                        if isinstance(target, basestring):
                            # maps one model field to one feed node
                            value = self.get_value(node, target)
                        elif isinstance(target, list):
                            # maps one model field to multiple feed nodes
                            value = self.join_fields(node, target)
                        elif isinstance(target, dict):
                            # maps one model field to a transformer method
                            transformer = getattr(instance, target['transformer'])
                            text_list = [self.get_value(node, target_field) for target_field in target['fields']]
                            value = transformer(*text_list)
                        setattr(instance, field, value)
                instance.save()


class AtomParser(XMLParser):
    "An XML parser for the Atom standard."

    def __init__(self, mapping):
        super(AtomParser, self).__init__(mapping)
        self.nsmap = {'atom': 'http://www.w3.org/2005/Atom'}


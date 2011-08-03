from django.db.models import get_model


class XMLParser(object):
    "Basic XML to Django model parser"

    def __init__(self, mapping):
        self.mapping = mapping

    def validate_model_format(self, model_string):
        "Validate that a model in the JSON mapping are in the format app.model."
        if not '.' in model_string or model_string.count('.') > 1:
            return False
        return True

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
        model_mappings = self.mapping.data_map['models']
        for model_string, configuration in model_mappings.items():
            if not self.validate_model_format(model_string):
                raise ValueError("Invalid model format in JSON mapping: %s" % model_string)
            model = get_model(*model_string.split("."))
            identifier = configuration['identifier']
            fields = configuration['fields']
            instance = model()
            for field, target in fields.items():
                # perform logic to determine type of mapping (one to one, one to many, one to transformer)
                if isinstance(target, basestring):
                    print "%s is mapped to one field" % field
                elif isinstance(target, list):
                    print "%s is mapped to many fields" % field
                elif isinstance(target, dict):
                    print "%s is mapped using a transformer" % field
                setattr(instance, field, target)
            #instance.save()
            print instance


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

    def grab_models(self):
        model_strings = self.mapping.data_map['models'].keys()
        for model_string in model_strings:
            if not self.validate_model_format(model_string):
                raise ValueError("Invalid model format in JSON mapping: %s" % model_string)
        return [get_model(*model_string.split('.')) for model_string in model_strings]

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
        pass


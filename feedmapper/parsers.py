from django.db.models import get_model


class XMLParser(object):
    "Basic XML to Django model parser"

    def __init__(self, mapping):
        self.mapping = mapping

    def grab_models(self):
        raw_models = self.mapping.data_map['models'].keys()
        return [get_model(*model.split('.')) for model in raw_models]


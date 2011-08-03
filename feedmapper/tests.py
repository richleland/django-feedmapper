from django.contrib.auth.models import User, Group
from django.test import TestCase

from .models import Mapping
from .parsers import XMLParser


class FeedMapperTests(TestCase):
    fixtures = ['test_data.json']

    def setUp(self):
        self.mapping = Mapping.objects.get(pk=1)
        self.parser = XMLParser(self.mapping)

    def test_parser_grabs_models(self):
        "Ensure the parser can grab the models from the JSON mapping."
        models = [User, Group]
        parsed_models = self.parser.grab_models()
        self.assertEqual(models, parsed_models)

    def test_model_format_validation_passes(self):
        "Ensure that validation passes if JSON mapping models are formatted properly."
        model_strings = ['myapp.MyModel', 'myapp.AnotherModel']
        self.assertTrue(self.parser.validate_model_format(model_strings))

    def test_model_format_validation_fails(self):
        "Ensure that validation fails if JSON mapping models are formatted improperly."
        model_strings = ['myapp.fail.MyModel', 'fail.myapp.AnotherModel']
        self.assertFalse(self.parser.validate_model_format(model_strings))

    def test_parser_grabs_fields(self):
        "Ensure the parser can grab the fields from the JSON mapping."
        pass

    def test_parser_handles_nodepath(self):
        "Ensure the parser can handle JSON with nodePath specified in it."
        pass

    def test_parser_one_to_one(self):
        "Ensure the parser can handle a one-to-one model field to feed node mapping."
        pass

    def test_parser_one_to_attribute(self):
        "Ensure the parser can handle a model field to feed node attribute mapping."
        pass

    def test_parser_one_to_many(self):
        "Ensure the parser can handle a one-to-many model field to feed nodes mapping."
        pass

    def test_parser_one_to_transformer(self):
        "Ensure the parser can handle a custom transformer for a model field."
        pass

    def test_parser_overwrites_items(self):
        "Ensure the parser overwrites items when sync type is set to OVERWRITE."
        pass

    def test_parser_updates_items(self):
        "Ensure the parser updates items when sync type is set to UPDATE."
        pass

    def test_parser_update_impossible(self):
        """
        Ensure that if the identifier isn't specified in a mapping and sync type is
        set to UPDATE the parsing is aborted.
        """
        pass

    def tearDown(self):
        pass

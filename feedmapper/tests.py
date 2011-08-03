from django.test import TestCase


class FeedMapperTests(TestCase):
    def setUp(self):
        pass

    def test_parser_grabs_models(self):
        "Ensure the parser can grab the models from the JSON mapping."
        pass

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

import os

from django.db import models
from django.test import TestCase

from feedmapper.models import Mapping
from feedmapper.parsers import XMLParser


TEST_DIR = os.path.abspath(os.path.dirname(__file__))


class AtomEntry(models.Model):
    "Dummy model for testing an Atom feed."
    atom_id = models.CharField(max_length=255, primary_key=True)
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)


class Thing(models.Model):
    "Dummy model for testing."
    email = models.EmailField()
    name = models.CharField(max_length=255)
    nick = models.CharField(max_length=50)
    combined = models.TextField()

    def convert_name(self, first_name, last_name):
        return "%s %s" % (first_name, last_name)


class FeedMapperTests(TestCase):
    fixtures = ['test_data.json']

    def setUp(self):
        self.mapping = Mapping.objects.get(pk=1)
        self.mapping.source = os.path.join(TEST_DIR, "dummy1.xml")
        self.mapping.parse()
        self.parser = XMLParser(self.mapping)

        self.atom_mapping = Mapping.objects.get(pk=3)
        self.atom_mapping.source = os.path.join(TEST_DIR, "atom.xml")
        self.atom_mapping.parse()

    def test_model_format_validation_passes(self):
        "Ensure that validation passes if JSON mapping models are formatted properly."
        model_string = 'myapp.MyModel'
        self.assertTrue(self.parser.validate_model_format(model_string))

    def test_model_format_validation_fails(self):
        "Ensure that validation fails if JSON mapping models are formatted improperly."
        model_string = 'myapp.fail.MyModel'
        self.assertFalse(self.parser.validate_model_format(model_string))

    def test_parser_one_to_one(self):
        "Ensure the parser can handle a one-to-one model field to feed node mapping."
        thing = Thing.objects.get(pk=1)
        self.assertEqual(thing.email, "vader@sith.org")

    def test_parser_one_to_attribute(self):
        "Ensure the parser can handle a model field to feed node attribute mapping."
        thing = Thing.objects.get(pk=1)
        self.assertEqual(thing.nick, "zeke")

    def test_parser_one_to_many(self):
        "Ensure the parser can handle a one-to-many model field to feed nodes mapping."
        thing = Thing.objects.get(pk=1)
        self.assertEqual(thing.combined, "vader@sith.org Anakin Skywalker")

    def test_parser_one_to_transformer(self):
        "Ensure the parser can handle a custom transformer for a model field."
        thing = Thing.objects.get(pk=1)
        self.assertEqual(thing.name, "Anakin Skywalker")

    def test_parser_purges_items(self):
        "Ensure the parser purges items when purging is enabled."
        num_things_before = Thing.objects.count()
        self.mapping.source = os.path.join(TEST_DIR, "dummy2.xml")
        self.mapping.purge = True
        self.mapping.parse()
        num_things_after = Thing.objects.count()
        self.assertEqual(num_things_before, 2)
        self.assertEqual(num_things_after, 1)

    def test_parser_updates_items(self):
        "Ensure the parser updates items when purging is disabled."
        num_things_before = Thing.objects.count()
        self.mapping.source = os.path.join(TEST_DIR, "dummy2.xml")
        self.mapping.parse()
        num_things_after = Thing.objects.count()
        self.assertEqual(num_things_before, num_things_after)

    def test_parser_update_impossible(self):
        "Ensure that a mapping without identifiers and purge turned off fails."
        mapping = Mapping.objects.get(pk=2)
        mapping.source = os.path.join(TEST_DIR, "exceptions.xml")
        self.assertRaises(UserWarning, mapping.parse)

    def test_parser_handles_local_files(self):
        "Ensure that the parser can handle a local filesystem data source."
        mapping = Mapping.objects.get(pk=1)
        mapping.source = "dummy1.xml"
        mapping.parse()
        thing = Thing.objects.get(pk=1)
        self.assertEqual(thing.name, "Anakin Skywalker")
        self.assertEqual(thing.nick, "zeke")
        self.assertEqual(thing.email, "vader@sith.org")
        self.assertEqual(thing.combined, "vader@sith.org Anakin Skywalker")

    def test_parser_handles_urls(self):
        "Ensure that the parser can handle a remote data source URL."
        mapping = Mapping.objects.get(pk=1)
        mapping.source = "http://a.com/notreal.xml"
        parser = XMLParser(mapping)
        self.assertEqual(parser.data_source, mapping.source)

    def test_xml_syntax_exception(self):
        mapping = Mapping.objects.get(pk=1)
        mapping.source = os.path.join(TEST_DIR, "malformed.xml")
        mapping.parse()
        self.assertTrue("feedmapper/tests/malformed.xml:6:27:FATAL:PARSER:ERR_ATTRIBUTE_NOT_STARTED" in mapping.parse_log)
        self.assertFalse(mapping.parse_succeeded)

    def test_bad_url_exception(self):
        mapping = Mapping.objects.get(pk=1)
        mapping.source = "http://a.com/notreal.xml"
        mapping.parse()
        self.assertEqual(mapping.parse_log, u'Error reading file \'http://a.com/notreal.xml\': failed to load external entity "http://a.com/notreal.xml"')
        self.assertFalse(mapping.parse_succeeded)

    def tearDown(self):
        pass


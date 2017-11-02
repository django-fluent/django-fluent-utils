import django
from django.core.exceptions import ImproperlyConfigured
from django.test import SimpleTestCase

from fluent_utils.load import import_module_or_none, import_class, import_settings_class, \
    import_apps_submodule


class LoadTests(SimpleTestCase):

    def test_import_apps_submodule(self):
        expected = ['django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sites']
        self.assertEqual(import_apps_submodule('admin'), expected)

    def test_import_settings_class(self):
        self.assertIsNotNone(import_settings_class('TEST_RUNNER'))

    def test_import_class(self):
        self.assertIs(import_class('fluent_utils.tests.test_load.LoadTests'), LoadTests)
        self.assertRaises(ImproperlyConfigured, lambda: import_class('fluent_utils.tests.test_load.InvalidLoadTests'))

    def test_ignore_top_level(self):
        self.assertIsNone(import_module_or_none("non_existant"))

    def test_detect_sub_import_error(self):
        self.assertRaises(ImportError, lambda: import_module_or_none("fluent_utils.tests.import_test"))

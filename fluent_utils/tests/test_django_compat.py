from django.test import SimpleTestCase


class DjangoCompatTests(SimpleTestCase):
    def test_import(self):
        import fluent_utils.django_compat  # noqa

"""
Optional integration with django-any-urlfield
"""
from __future__ import absolute_import

from django.db import models

from fluent_utils.django_compat import is_installed

if is_installed('any_urlfield'):
    from any_urlfield.models import AnyUrlField as BaseUrlField
else:
    BaseUrlField = models.URLField


# subclassing here so South or Django migrations detect a single class.
class AnyUrlField(BaseUrlField):
    """
    A CharField that can either refer to a CMS page ID, or external URL.

    If *django-any-urlfield* is not installed, only regular URLs can be used.
    """

    def __init__(self, *args, **kwargs):
        if 'max_length' not in kwargs:
            kwargs['max_length'] = 300  # Standardize
        super(AnyUrlField, self).__init__(*args, **kwargs)

    def south_field_triple(self):
        # Masquerade as normal URLField, so the soft-dependency also exists in the migrations.
        from south.modelsinspector import introspector
        path = "{0}.{1}".format(models.URLField.__module__, models.URLField.__name__)
        args, kwargs = introspector(self)
        return (path, args, kwargs)

    def deconstruct(self):
        # For Django 1.7 migrations, masquerade as normal URLField too
        name, path, args, kwargs = super(AnyUrlField, self).deconstruct()
        return name, "django.db.models.URLField", args, kwargs

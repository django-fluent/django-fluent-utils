"""Obsolete django-compatibility module.
This is no longer needed in django-fluent-* >= 3.0 which only supports Django 2.2 and up.
"""

# django-fluent-pages 3.0 still imported this from here:
from django.db.models.fields.related import ForwardManyToOneDescriptor

from .fluent_compat import is_installed  # used by many apps

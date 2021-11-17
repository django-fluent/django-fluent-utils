"""
Optional integration with django-any-urlfield
"""

from django.db import models

from fluent_utils.django_compat import is_installed

if is_installed("any_urlfield"):
    from any_urlfield.models import AnyUrlField as BaseUrlField
else:
    BaseUrlField = models.URLField


# subclassing here so Django migrations detect a single class.
class AnyUrlField(BaseUrlField):
    """
    A CharField that can either refer to a CMS page ID, or external URL.

    If *django-any-urlfield* is not installed, only regular URLs can be used.
    """

    def __init__(self, *args, **kwargs):
        if "max_length" not in kwargs:
            kwargs["max_length"] = 300  # Standardize
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        # For Django 1.7 migrations, masquerade as normal URLField too
        name, path, args, kwargs = super().deconstruct()
        return name, "django.db.models.URLField", args, kwargs

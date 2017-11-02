"""
Optional integration with django-any-Imagefield
"""
from __future__ import absolute_import

from django.db import models

from fluent_utils.django_compat import is_installed

if is_installed('any_imagefield'):
    from any_imagefield.models import AnyFileField as BaseFileField, AnyImageField as BaseImageField
else:
    BaseFileField = models.FileField
    BaseImageField = models.ImageField


# subclassing here so South or Django migrations detect a single class.
class AnyFileField(BaseFileField):
    """
    A FileField that can refer to an uploaded file.

    If *django-any-imagefield* is not installed, the filebrowser link will not be displayed.
    """

    def deconstruct(self):
        # For Django migrations, masquerade as normal FileField too
        name, path, args, kwargs = super(AnyFileField, self).deconstruct()

        # FileField behavior
        if kwargs.get("max_length") == 100:
            del kwargs["max_length"]
        kwargs['upload_to'] = getattr(self, 'upload_to', None) or getattr(self, 'directory', None) or ''

        return name, "django.db.models.FileField", args, kwargs


# subclassing here so South or Django migrations detect a single class.
class AnyImageField(BaseImageField):
    """
    An ImageField that can refer to an uploaded image file.

    If *django-any-imagefield* is not installed, the filebrowser link will not be displayed.
    """

    def deconstruct(self):
        # For Django migrations, masquerade as normal ImageField too
        name, path, args, kwargs = super(AnyImageField, self).deconstruct()

        # FileField behavior
        if kwargs.get("max_length") == 100:
            del kwargs["max_length"]
        kwargs['upload_to'] = getattr(self, 'upload_to', None) or getattr(self, 'directory', None) or ''

        return name, "django.db.models.ImageField", args, kwargs

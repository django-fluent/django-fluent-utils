"""
Optional integration with django-taggit.
"""
from django.db import models
from fluent_utils.django_compat import is_installed

__all__ = (
    'TaggableManager',
    'TagsMixin',
)

TaggableManager = None

if is_installed('taggit_autosuggest'):
    from taggit_autosuggest.managers import TaggableManager
elif is_installed('taggit_autocomplete_modified'):
    from taggit_autocomplete_modified.managers import TaggableManagerAutocomplete as TaggableManager
elif is_installed('taggit'):
    from taggit.managers import TaggableManager


# Make sure the 'tags' field is ignored by old versions of South
try:
    from south.modelsinspector import add_ignored_fields
except ImportError:
    pass
else:
    # South should ignore the tags field as it's a RelatedField.
    add_ignored_fields((
        "^taggit\.managers\.TaggableManager",
        "^taggit_autosuggest\.managers\.TaggableManager",
        "^taggit_autocomplete_modified\.managers\.TaggableManagerAutocomplete",
    ))


class TagsMixin(models.Model):
    """
    Mixin for adding tags to a model.
    """
    # Make association with tags optional.
    if TaggableManager is not None:
        tags = TaggableManager(blank=True)
    else:
        tags = None

    class Meta:
        abstract = True

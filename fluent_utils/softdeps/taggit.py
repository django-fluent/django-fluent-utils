"""
Optional integration with django-taggit.
"""
from __future__ import absolute_import

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Field

from fluent_utils.django_compat import is_installed

__all__ = (
    'TaggableManager',
    'TagsMixin',
)

if is_installed('taggit_selectize'):
    from taggit_selectize.managers import TaggableManager as BaseTaggableManager
elif is_installed('taggit_autosuggest'):
    from taggit_autosuggest.managers import TaggableManager as BaseTaggableManager
elif is_installed('taggit_autocomplete_modified'):
    from taggit_autocomplete_modified.managers import TaggableManagerAutocomplete as BaseTaggableManager
elif is_installed('taggit'):
    from taggit.managers import TaggableManager as BaseTaggableManager
else:
    BaseTaggableManager = None


# Make sure the 'tags' field is ignored by old versions of South
try:
    from south.modelsinspector import add_ignored_fields
except ImportError:
    pass
else:
    # South should ignore the tags field as it's a RelatedField.
    add_ignored_fields((
        "^taggit\.managers\.TaggableManager",
        "^taggit_selectize\.managers\.TaggableManager",
        "^taggit_autosuggest\.managers\.TaggableManager",
        "^taggit_autocomplete_modified\.managers\.TaggableManagerAutocomplete",
    ))


if BaseTaggableManager is not None:
    # Make sure the migrations have one consistent path to import from
    class TaggableManager(BaseTaggableManager):
        pass
else:
    class TaggableManager(Field):
        def __bool__(self):
            return False  # partial compatibility with old code.

        def __nonzero__(self):
            return False  # Python 2

        def contribute_to_class(self, cls, name, *args, **kwargs):
            setattr(cls, name, None)  # compatibility with old code.

        def db_type(self, connection):
            return None  # just like RelatedField


class TagsMixin(models.Model):
    """
    Mixin for adding tags to a model.
    """
    # Make association with tags optional.
    tags = TaggableManager(blank=True)

    class Meta:
        abstract = True

    def similar_objects(self, num=None, **filters):
        """
        Find similar objects using related tags.
        """
        tags = self.tags
        if not tags:
            return []

        content_type = ContentType.objects.get_for_model(self.__class__)
        filters['content_type'] = content_type

        # can't filter, see
        # - https://github.com/alex/django-taggit/issues/32
        # - https://django-taggit.readthedocs.io/en/latest/api.html#TaggableManager.similar_objects
        #
        # Otherwise this would be possible:
        # return tags.similar_objects(**filters)

        lookup_kwargs = tags._lookup_kwargs()
        lookup_keys = sorted(lookup_kwargs)
        qs = tags.through.objects.values(*lookup_kwargs.keys())
        qs = qs.annotate(n=models.Count('pk'))
        qs = qs.exclude(**lookup_kwargs)
        subq = tags.all()
        qs = qs.filter(tag__in=list(subq))
        qs = qs.order_by('-n')

        # from https://github.com/alex/django-taggit/issues/32#issuecomment-1002491
        if filters is not None:
            qs = qs.filter(**filters)

        if num is not None:
            qs = qs[:num]

        # Normal taggit code continues

        # TODO: This all feels like a bit of a hack.
        items = {}
        if len(lookup_keys) == 1:
            # Can we do this without a second query by using a select_related()
            # somehow?
            f = tags.through._meta.get_field_by_name(lookup_keys[0])[0]
            objs = f.rel.to._default_manager.filter(**{
                "%s__in" % f.rel.field_name: [r["content_object"] for r in qs]
            })
            for obj in objs:
                items[(getattr(obj, f.rel.field_name),)] = obj
        else:
            preload = {}
            for result in qs:
                preload.setdefault(result['content_type'], set())
                preload[result["content_type"]].add(result["object_id"])

            for ct, obj_ids in preload.items():
                ct = ContentType.objects.get_for_id(ct)
                for obj in ct.model_class()._default_manager.filter(pk__in=obj_ids):
                    items[(ct.pk, obj.pk)] = obj

        results = []
        for result in qs:
            obj = items[
                tuple(result[k] for k in lookup_keys)
            ]
            obj.similar_tags = result["n"]
            results.append(obj)
        return results

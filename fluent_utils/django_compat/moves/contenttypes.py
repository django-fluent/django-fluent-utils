try:
    # Django 1.7
    from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation, GenericRel
except ImportError:
    from django.contrib.contenttypes.generic import GenericForeignKey, GenericRelation, GenericRel

__all__ = (
    'GenericForeignKey',
    'GenericRelation',
    'GenericRel',
)

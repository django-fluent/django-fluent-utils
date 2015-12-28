try:
    from django.db.models.fields.related import ReverseOneToOneDescriptor, ForwardManyToOneDescriptor
except ImportError:
    # django < 1.9
    from django.db.models.fields.related import (
        SingleRelatedObjectDescriptor as ReverseOneToOneDescriptor,
        ReverseSingleRelatedObjectDescriptor as ForwardManyToOneDescriptor,
    )

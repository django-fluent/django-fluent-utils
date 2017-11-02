from django.db import models


class HideChoicesCharField(models.CharField):
    """
    For Django 1.7, hide the 'choices' for a field.
    """

    def deconstruct(self):
        name, path, args, kwargs = models.CharField.deconstruct(self)

        # Hide the fact this model was used.
        if path == 'fluent_utils.dry.fields.HideChoicesCharField':
            path = 'django.db.models.CharField'
        try:
            del kwargs['choices']
        except KeyError:
            pass

        return name, path, args, kwargs

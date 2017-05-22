# Support for custom User models in Django 1.5+
from django.conf import settings

try:
    from django.contrib.auth import get_user_model
    AUTH_USER_MODEL = settings.AUTH_USER_MODEL
except ImportError:
    # django < 1.5
    from django.contrib.auth.models import User

    def get_user_model():
        return User

    AUTH_USER_MODEL = '{0}.{1}'.format(User._meta.app_label, User._meta.object_name)

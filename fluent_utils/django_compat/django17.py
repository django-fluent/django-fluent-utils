import sys
from django.conf import settings


try:
    from django.apps import apps
except ImportError:
    from django.db.backends.util import truncate_name

    # Django 1.6 or below.
    def is_installed(appname):
        return appname in settings.INSTALLED_APPS

    from django.db.models import get_models

    def get_app_names():
        return settings.INSTALLED_APPS

    def get_app_label(module):
        # Django <= 1.6 does not know apps.
        # Figure out the app_label by looking one level up.
        # For 'django.contrib.sites.models', this would be 'sites'.
        model_module = sys.modules[module]
        return model_module.__name__.split('.')[-2]

    def get_meta_model_name(opts):
        return opts.module_name

else:
    # util was renamed to utils for consistently
    from django.db.backends.utils import truncate_name

    # Django 1.7 provides an official API, and INSTALLED_APPS may contain non-string values too.
    is_installed = apps.is_installed
    get_models = apps.get_models

    def get_app_names():
        return [
            appconfig.name for appconfig in apps.get_app_configs()
        ]

    def get_app_label(module):
        # Django 1.7 knows the "apps", so it can provide the meta information
        app_config = apps.get_containing_app_config(module)
        return app_config.label

    def get_meta_model_name(opts):
        # This name was available as of Django 1.6, mandatory in 1.8
        return opts.model_name

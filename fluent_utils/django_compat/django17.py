import logging
import sys

from django.conf import settings

logger = logging.getLogger(__name__)


try:
    from django.apps import apps
except ImportError:
    from django.db.backends.util import truncate_name
    from django.db.models.loading import get_model
    from django.contrib.sites.models import get_current_site

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

    # get_current_site was moved outside models to avoid import Site models
    from django.contrib.sites.shortcuts import get_current_site

    # Django 1.7 provides an official API, and INSTALLED_APPS may contain non-string values too.
    get_models = apps.get_models
    get_model = apps.get_model

    def is_installed(appname):
        if apps.apps_ready:
            return apps.is_installed(appname)
        else:
            logger.debug('''fluent_utils.django_compat.is_installed("%s") only checks settings.INSTALLED_APPS, Apps aren't loaded yet.''', appname)
            return appname in settings.INSTALLED_APPS

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

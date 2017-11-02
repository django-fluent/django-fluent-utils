"""
This module collects all removed Django compatibility logic,
but retains the old import so it doesn't break existing django-fluent packages.
"""
import logging

from django.apps import apps
from django.conf import settings
from django.db import transaction
from django.db.models.query import EmptyQuerySet
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters  # noqa
from django.contrib.auth import get_user_model  # noqa
from django.contrib.sites.shortcuts import get_current_site  # noqa
from django.db.backends.utils import truncate_name  # noqa
from django.utils.encoding import smart_text  # noqa

logger = logging.getLogger(__name__)

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.user')

transaction_atomic = transaction.atomic
get_models = apps.get_models
get_model = apps.get_model


def is_queryset_empty(queryset):
    return isinstance(queryset, EmptyQuerySet)


def is_installed(appname):
    # for old django-fluent compatibility
    if apps.apps_ready:
        return apps.is_installed(appname)
    else:
        logger.debug('''fluent_utils.django_compat.is_installed("%s") only checks settings.INSTALLED_APPS, Apps aren't loaded yet.''', appname)  # noqa
        return appname in settings.INSTALLED_APPS


def get_app_label(module):
    app_config = apps.get_containing_app_config(module)
    return app_config.label


def get_app_names():
    return [
        appconfig.name for appconfig in apps.get_app_configs()
    ]


def get_meta_model_name(opts):
    # This name was available as of Django 1.6, mandatory in 1.8
    return opts.model_name

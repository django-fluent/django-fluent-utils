from django.conf import settings

try:
    from django.apps import apps
except ImportError:
    # Django 1.6 or below.
    def is_installed(appname):
        return appname in settings.INSTALLED_APPS
else:
    # Django 1.7 provides an official API, and INSTALLED_APPS may contain non-string values too.
    is_installed = apps.is_installed

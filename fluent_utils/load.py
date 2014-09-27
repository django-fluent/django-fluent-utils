from __future__ import absolute_import
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
import sys
import traceback

try:
    from importlib import import_module
except ImportError:
    from django.utils.importlib import import_module  # Python 2.6 compatibility


__all__ = (
    'import_class',
    'import_apps_submodule',
)


def import_class(import_path, setting_name):
    """
    Import a class by name.
    """
    mod_name, class_name = import_path.rsplit('.', 1)

    # import module
    try:
        mod = import_module(mod_name)
        cls = getattr(mod, class_name)
    except ImportError as e:
        # ImportError does not provide easy way to distinguish those two cases.
        # Fortunately, the traceback of the ImportError starts at __import__
        # statement. If the traceback has more than one frame, it means that
        # application was found and ImportError originates within the local app
        __, __, exc_traceback = sys.exc_info()
        frames = traceback.extract_tb(exc_traceback)
        if len(frames) > 1:
            raise  # import error is a level deeper.

        raise ImproperlyConfigured("{0} does not point to an existing class: {1}".format(setting_name, import_path))
    except AttributeError:
        raise ImproperlyConfigured("{0} does not point to an existing class: {1}".format(setting_name, import_path))

    return cls


def import_apps_submodule(submodule):
    """
    Look for a submodule is a series of packages, e.g. ".pagetype_plugins" in all INSTALLED_APPS.
    """
    for app in settings.INSTALLED_APPS:
        try:
            import_module('.' + submodule, app)
        except ImportError:
            __, __, exc_traceback = sys.exc_info()
            frames = traceback.extract_tb(exc_traceback)
            if len(frames) > 1:
                raise  # import error is a level deeper.
            else:
                pass

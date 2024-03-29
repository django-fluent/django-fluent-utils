import importlib
import os
import sys
import traceback

from django.apps import apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

__all__ = (
    "import_settings_class",
    "import_class",
    "import_apps_submodule",
)

# Windows support
IMPORT_PATH_IMPORTLIB = importlib.__file__.rstrip("c")  # .pyc -> .py
IMPORT_PATH_GEVENT = os.path.join("gevent", "builtins.py")
IMPORT_PATH_PYDEV = os.path.sep + "_pydev_"


def import_settings_class(setting_name):
    """
    Return the class pointed to be an app setting variable.
    """
    config_value = getattr(settings, setting_name)
    if config_value is None:
        raise ImproperlyConfigured(f"Required setting not found: {setting_name}")

    return import_class(config_value, setting_name)


def import_class(import_path, setting_name=None):
    """
    Import a class by name.
    """
    mod_name, class_name = import_path.rsplit(".", 1)

    # import module
    mod = import_module_or_none(mod_name)
    if mod is not None:
        # Loaded module, get attribute
        try:
            return getattr(mod, class_name)
        except AttributeError:
            pass

    # For ImportError and AttributeError, raise the same exception.
    if setting_name:
        raise ImproperlyConfigured(
            f"{setting_name} does not point to an existing class: {import_path}"
        )
    else:
        raise ImproperlyConfigured(f"Class not found: {import_path}")


def import_apps_submodule(submodule):
    """
    Look for a submodule is a series of packages, e.g. ".pagetype_plugins" in all INSTALLED_APPS.
    """
    found_apps = []
    for appconfig in apps.get_app_configs():
        app = appconfig.name
        if import_module_or_none(f"{app}.{submodule}") is not None:
            found_apps.append(app)

    return found_apps


def import_module_or_none(module_label):
    """
    Imports the module with the given name.

    Returns None if the module doesn't exist,
    but it does propagates import errors in deeper modules.
    """
    try:
        # On Python 3, importlib has much more functionality compared to Python 2.
        return importlib.import_module(module_label)
    except ImportError:
        # Based on code from django-oscar:
        # There are 2 reasons why there could be an ImportError:
        #
        #  1. Module does not exist. In that case, we ignore the import and return None
        #  2. Module exists but another ImportError occurred when trying to import the module.
        #     In that case, it is important to propagate the error.
        #
        # ImportError does not provide easy way to distinguish those two cases.
        # Fortunately, the traceback of the ImportError starts at __import__
        # statement. If the traceback has more than one frame, it means that
        # application was found and ImportError originates within the local app
        __, __, exc_traceback = sys.exc_info()
        frames = traceback.extract_tb(exc_traceback)
        frames = [
            f
            for f in frames
            if f[0] != "<frozen importlib._bootstrap>"
            and f[0] != IMPORT_PATH_IMPORTLIB  # Python 3.6
            and not f[0].endswith(IMPORT_PATH_GEVENT)
            and not IMPORT_PATH_PYDEV in f[0]
        ]
        if len(frames) > 1:
            raise
    return None

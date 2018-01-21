from .django19 import ReverseOneToOneDescriptor, ForwardManyToOneDescriptor
from .django110 import MiddlewareMixin
from .django20 import reverse, resolve, Resolver404, NoReverseMatch, get_urlconf, set_urlconf, get_script_prefix, set_script_prefix
from .fluent_compat import add_preserved_filters, smart_text, truncate_name, AUTH_USER_MODEL, get_models, get_model, get_app_label, get_app_names, get_user_model, is_queryset_empty, get_current_site, get_meta_model_name, is_installed

__all__ = (
    'get_user_model', 'AUTH_USER_MODEL',
    'add_preserved_filters',
    'is_queryset_empty',
    'is_installed', 'get_models', 'get_model', 'get_app_names', 'get_app_label', 'truncate_name', 'get_meta_model_name', 'get_current_site',
    'ReverseOneToOneDescriptor', 'ForwardManyToOneDescriptor',
    'MiddlewareMixin',
    'reverse', 'resolve', 'Resolver404', 'NoReverseMatch', 'set_urlconf', 'get_urlconf', 'get_script_prefix', 'set_script_prefix',
    'smart_text',
)

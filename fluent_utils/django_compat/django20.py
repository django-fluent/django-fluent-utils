try:
    # As of Django 1.10 these are available
    from django.urls import reverse, resolve, Resolver404, NoReverseMatch, get_urlconf, set_urlconf, get_script_prefix, set_script_prefix
except ImportError:
    from django.core.urlresolvers import reverse, resolve, Resolver404, NoReverseMatch, get_urlconf, set_urlconf, get_script_prefix, set_script_prefix

"""
Optional integration with fluent-pages features
"""
from __future__ import absolute_import

from django.utils.functional import lazy

from fluent_utils.django_compat import is_installed

__all__ = (
    'CurrentPageMixin',
    'mixed_reverse',
    'mixed_reverse_lazy',
    'HAS_APP_URLS',
)

if is_installed('fluent_pages'):
    # Use the real code.
    from fluent_pages.views import CurrentPageMixin
    from fluent_pages.urlresolvers import mixed_reverse  # app_reverse == hard dependency, no need to import here.

    try:
        from fluent_pages.urlresolvers import mixed_reverse_lazy  # added after v1.0b4
    except ImportError:
        mixed_reverse_lazy = lazy(mixed_reverse, str)

    HAS_APP_URLS = True
else:
    # Use the stubs
    from fluent_utils.django_compat import is_installed, reverse

    try:
        from parler.views import ViewUrlMixin
    except ImportError:
        ViewUrlMixin = object

    HAS_APP_URLS = False

    class CurrentPageMixin(ViewUrlMixin):
        """
        Sub for CurrentPageMixin. Will use the real code if it exists.
        Make sure to define :attr:`view_url_name`, as that is required by :class:`~parler.views.ViewUrlMixin`.
        """
        pass

    def mixed_reverse(viewname, args=None, kwargs=None, current_app=None, current_page=None, language_code=None, multiple=False, ignore_multiple=False):
        """
        Stub for :func:`fluent_pages.urlresolvers.mixed_reverse`.
        Will use the real code if the app is loaded,
        otherwise :func:`~django.urls.reverse` is used.
        """
        return reverse(viewname, args=args, kwargs=kwargs, current_app=current_app)

    mixed_reverse_lazy = lazy(mixed_reverse, str)

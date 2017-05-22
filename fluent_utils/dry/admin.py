import django
from django.conf import settings


class MultiSiteAdminMixin(object):
    """
    Filter the models by ``parent_site``.
    """
    filter_site = True

    def get_queryset(self, request):
        qs = super(MultiSiteAdminMixin, self).get_queryset(request)

        # Admin only shows current site for now,
        # until there is decent filtering for it.
        if self.filter_site:
            qs = qs.parent_site(int(settings.SITE_ID))  # Note: that method can be customized (e.g. SharedContentQuerySet)
        return qs

    # For Django 1.5:
    # Leave for Django 1.6/1.7, so backwards compatibility can be fixed.
    # It will be removed in Django 1.8, so remove it here too to avoid false promises.
    if django.VERSION < (1, 8):
        def queryset(self, request):
            qs = super(MultiSiteAdminMixin, self).queryset(request)
            if self.filter_site:
                qs = qs.parent_site(int(settings.SITE_ID))
            return qs

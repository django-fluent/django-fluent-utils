from django.conf import settings


class MultiSiteAdminMixin:
    """
    Filter the models by ``parent_site``.
    """

    filter_site = True

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Admin only shows current site for now,
        # until there is decent filtering for it.
        if self.filter_site:
            qs = qs.parent_site(
                int(settings.SITE_ID)
            )  # Note: that method can be customized (e.g. SharedContentQuerySet)
        return qs

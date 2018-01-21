"""
Optional integration with django-contrib-comments

This avoids loading django_comments or django.contrib.comments unless it's installed.
All functions even work without having the app installed,
and return stub or dummy values so all code works as expected.
"""
import django
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.db import models
from django.dispatch import Signal
from django.utils.translation import ugettext_lazy as _

from fluent_utils.django_compat import is_installed

__all__ = (
    'django_comments',                # Main module
    'signals',                        # Signals module
    'get_model',                      # Get the comment model
    'get_form',                       # Get the comment form
    'get_public_comments_for_model',  # Get publicly visible comments
    'get_comments_are_open',          # Utility to check if comments are open for a model.
    'get_comments_are_moderated',     # Utility to check if comments are moderated for a model.
    'CommentModel',                   # Points to the comments model.
    'CommentModerator',               # Base class for all custom comment moderators
    'CommentsRelation',               # Generic relation back to the comments.
    'CommentsMixin',                  # Model mixin for comments
    'IS_INSTALLED',
)

django_comments = None
moderator = None
CommentModerator = None
get_model = None
IS_INSTALLED = False

if is_installed('django.contrib.comments'):
    # Django 1.7 and below
    from django.contrib import comments as django_comments
    from django.contrib.comments import get_model, get_form, signals
    from django.contrib.comments.moderation import moderator, CommentModerator
    IS_INSTALLED = True
elif is_installed('django_comments'):
    # as of Django 1.8, this is a separate app.
    import django_comments
    from django_comments import get_model, get_form, signals
    from django_comments.moderation import moderator, CommentModerator
    IS_INSTALLED = True
else:
    def get_model():
        return CommentManagerStub

    def get_form():
        raise NotImplementedError("No stub for comments.get_form() is implemented!")

    class SignalsStub(object):
        comment_will_be_posted = Signal(providing_args=["comment", "request"])
        comment_was_posted = Signal(providing_args=["comment", "request"])
        comment_was_flagged = Signal(providing_args=["comment", "flag", "created", "request"])

    signals = SignalsStub()


def get_public_comments_for_model(model):
    """
    Get visible comments for the model.
    """
    if not IS_INSTALLED:
        # No local comments, return empty queryset.
        # The project might be using DISQUS or Facebook comments instead.
        return CommentModelStub.objects.none()
    else:
        return CommentModel.objects.for_model(model).filter(is_public=True, is_removed=False)


def get_comments_are_open(instance):
    """
    Check if comments are open for the instance
    """
    if not IS_INSTALLED:
        return False

    try:
        # Get the moderator which is installed for this model.
        mod = moderator._registry[instance.__class__]
    except KeyError:
        # No moderator = no restrictions
        return True

    # Check the 'enable_field', 'auto_close_field' and 'close_after',
    # by reusing the basic Django policies.
    return CommentModerator.allow(mod, None, instance, None)


def get_comments_are_moderated(instance):
    """
    Check if comments are moderated for the instance
    """
    if not IS_INSTALLED:
        return False

    try:
        # Get the moderator which is installed for this model.
        mod = moderator._registry[instance.__class__]
    except KeyError:
        # No moderator = no moderation
        return False

    # Check the 'auto_moderate_field', 'moderate_after',
    # by reusing the basic Django policies.
    return CommentModerator.moderate(mod, None, instance, None)


# Can't use EmptyQueryset stub in Django 1.6 anymore,
# using this model to build a queryset instead.
class CommentManagerStub(models.Manager):
    # Tell Django that related fields also need to use this manager:
    # This makes sure that deleting a User won't cause any SQL queries
    # on a non-existend django_comments_stub table.
    use_for_related_fields = True

    def get_queryset(self):
        return super(CommentManagerStub, self).get_queryset().none()

    if django.VERSION < (1, 7):
        def get_query_set(self):
            return super(CommentManagerStub, self).get_query_set().none()

    def in_moderation(self):
        return self.none()

    def for_model(self):
        return self.none()


class CommentModelStub(models.Model):
    """
    Stub model that :func:`get_model` returns if *django.contrib.comments* is not installed.
    """
    class Meta:
        managed = False
        app_label = 'django_comments'
        db_table = "django_comments_stub"

    objects = CommentManagerStub()

    # add fields so ORM queries won't cause any issues.
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_pk = models.TextField()
    content_object = GenericForeignKey(ct_field="content_type", fk_field="object_pk")
    site = models.ForeignKey(Site, on_delete=models.CASCADE)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, related_name="%(class)s_comments", on_delete=models.SET_NULL)
    user_name = models.CharField(max_length=50, blank=True)
    user_email = models.EmailField(blank=True)
    user_url = models.URLField(blank=True)
    comment = models.TextField(max_length=3000)
    submit_date = models.DateTimeField(default=None)
    ip_address = models.GenericIPAddressField(unpack_ipv4=True, blank=True, null=True)
    is_public = models.BooleanField(default=True)
    is_removed = models.BooleanField(default=False)


CommentModel = get_model()


if IS_INSTALLED:
    class CommentRelation(GenericRelation):

        def __init__(self, to=CommentModel, **kwargs):
            kwargs.setdefault('object_id_field', 'object_pk')
            super(CommentRelation, self).__init__(to, **kwargs)
else:
    class CommentRelation(models.Field):

        def __init__(self, *args, **kwargs):
            pass

        def contribute_to_class(self, cls, name, virtual_only=False):
            setattr(cls, name, CommentModelStub.objects.none())


class CommentsMixin(models.Model):
    """
    Mixin for adding comments support to a model.
    """
    enable_comments = models.BooleanField(_("Enable comments"), default=True)

    # Reverse relation to the comments model.
    # This is a stub when django.contrib.comments is not installed, so templates don't break.
    # This avoids importing django.contrib.comments models when the app is not used.
    all_comments = CommentRelation(verbose_name=_("Comments"))

    class Meta:
        abstract = True

    # Properties
    comments = property(get_public_comments_for_model, doc="Return the visible comments.")
    comments_are_moderated = property(get_comments_are_moderated, doc="Check if comments are moderated")

    @property
    def comments_are_open(self):
        """
        Check if comments are open
        """
        if not self.enable_comments:
            return False

        return get_comments_are_open(self)

# The timezone support was introduced in Django 1.4, fallback to standard library for 1.3.
try:
    from django.utils.timezone import now, utc
except ImportError:
    # Django < 1.4
    from datetime import datetime
    now = datetime.now
    utc = None   # datetime(..., tzinfo=utc) creates naive datetime this way.

# URLs moved in Django 1.4
try:
    # Django 1.6 requires this
    from django.conf.urls import patterns, url, include
except ImportError:
    # Django 1.3 compatibility, kept in minor release
    from django.conf.urls.defaults import patterns, url, include

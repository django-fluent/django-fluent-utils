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
    from django.conf.urls import url, include
except ImportError:
    # Django 1.3 compatibility, kept in minor release
    from django.conf.urls.defaults import patterns, url, include
else:
    try:
        from django.conf.urls import patterns  # Django 1.9-
    except ImportError:
        from django.core.urlresolvers import RegexURLPattern

        def patterns(prefix, *args):
            pattern_list = []
            for t in args:
                if isinstance(t, (list, tuple)):
                    t = url(prefix=prefix, *t)
                elif isinstance(t, RegexURLPattern):
                    t.add_prefix(prefix)
                pattern_list.append(t)
            return pattern_list

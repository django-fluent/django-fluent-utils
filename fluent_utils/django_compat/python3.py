try:
    # Python 3
    from django.utils.encoding import smart_text
except ImportError:
    try:
        from django.utils.encoding import smart_unicode as smart_text
    except ImportError:
        from django.forms.util import smart_unicode as smart_text


__all__ = (
    'smart_text',
)

django-fluent-utils
===================

Utility functions for code sharing between *django-fluent-..* modules.

This includes:

* Making integration with modules optional
* Django compatibility code
* Shared code for fluet apps ("Don't repeat yourself")

For optional modules, STUB interfaces are implemented.
When the actual modules are available, those features are picked up by all apps.

* django-fluent-pages_: ``CurrentPageMixin``, ``app_reverse()``, ``mixed_reverse()``.
* django-any-urlfield_: ``AnyUrlField`` enhances the standard Django ``URLField``.
* django-any-imagefield_: ``AnyImageField`` and ``AnyFileField`` enhance the standard Django ``ImageField`` and ``FileField``.
* django-taggit_: tagging can be added optionally, based on django-taggit_, django-taggit-autosuggest_ or django-taggit-autocomplete-modified_.
* django_comments_: commenting support can use django_comments_ or the older django.contrib.comments_.

This module is mainly used internally between other django-fluent apps.
For the whole list of apps, see http://django-fluent.org/

.. _django_comments: https://github.com/django/django-contrib-comments
.. _django.contrib.comments: https://docs.djangoproject.com/en/1.7/ref/contrib/comments/
.. _django-fluent-pages: https://github.com/edoburu/django-fluent-pages
.. _django-any-imagefield: https://github.com/edoburu/django-any-imagefield
.. _django-any-urlfield: https://github.com/edoburu/django-any-urlfield
.. _django-taggit: https://github.com/alex/django-taggit
.. _django-taggit-autosuggest: https://bitbucket.org/fabian/django-taggit-autosuggest
.. _django-taggit-autocomplete-modified: https://github.com/gnotaras/django-taggit-autocomplete-modified

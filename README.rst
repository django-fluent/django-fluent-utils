django-fluent-utils
===================

This module is mainly used internally between other django-fluent apps.
For the whole list of apps, see http://django-fluent.org/

This module provides:

* Stubs to make integration with third-party apps optional
* Django compatibility code
* Shared code for fluent apps ("Don't repeat yourself")


Stub features
-------------

``fluent_utils.softdeps.any_imagefield``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Support django-any-imagefield_ when it's available.
This provides an improved ``ImageField`` and ``FileField``.

It supports various third party media libraries,
allowing django-fluent to use the media library of your choice.


``fluent_utils.softdeps.any_urlfield``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``AnyUrlField`` enhances the standard Django ``URLField``, when django-any-urlfield_ is installed.


``fluent_utils.softdeps.comments``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Seemingly switch between django_comments_ or the older django.contrib.comments_.


``fluent_utils.softdeps.fluent_pages``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Stub the ``CurrentPageMixin``, ``app_reverse()`` and ``mixed_reverse()`` when django-fluent-pages_ is not installed.
This allows apps to revert to standard ``urls.py`` URLs when they can't provide URLs via a custom page type for the fluent-pages tree.


``fluent_utils.softdeps.taggit``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Optional support for tagging. It supports various applications:

* django-taggit_
* taggit-selectize_
* django-taggit-autosuggest_
* django-taggit-autocomplete-modified_

django-fluent automatically uses one of these third-party apps when it's found in ``INSTALLED_APPS``.


Internal API's
--------------

These API's are available for other *django-fluent-..* modules:

* ``fluent_utils.ajax.JsonResponse`` - a ``JsonResponse`` before Django 1.8 provided that.
* ``fluent_utils.django_compat`` - imports for various features that moved or changed between Django versions.
* ``fluent_utils.dry.admin.MultiSiteAdminMixin`` - mixin for the admin to filter on the ``parent_site`` field.
* ``fluent_utils.dry.fields.HideChoicesCharField`` - avoid expanding choices in Django migrations.
* ``fluent_utils.load.import_apps_submodule()`` - import a module in every application found in ``INSTALLED_APPS``.
* ``fluent_utils.load.import_class()`` - import a class via a Python path.
* ``fluent_utils.load.import_settings_class()`` - import a class via a named setting.
* ``fluent_utils.load.import_module_or_none()`` - import a module, only raises an ``ImportError`` for sub modules.
* ``fluent_utils.softdeps.*`` - various soft dependencies, see above


.. _django_comments: https://github.com/django/django-contrib-comments
.. _django.contrib.comments: https://docs.djangoproject.com/en/1.7/ref/contrib/comments/
.. _django-fluent-pages: https://github.com/edoburu/django-fluent-pages
.. _django-any-imagefield: https://github.com/edoburu/django-any-imagefield
.. _django-any-urlfield: https://github.com/edoburu/django-any-urlfield
.. _django-taggit: https://github.com/alex/django-taggit
.. _django-taggit-autosuggest: https://bitbucket.org/fabian/django-taggit-autosuggest
.. _django-taggit-autocomplete-modified: https://github.com/gnotaras/django-taggit-autocomplete-modified
.. _taggit-selectize: https://github.com/chhantyal/taggit-selectize

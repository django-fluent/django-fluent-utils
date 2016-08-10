Changelog
=========

Version 1.3 (2016-08-05)
------------------------

* Added support taggit-selectize_.
  When installed all fluent apps use this dependency.


Version 1.2.4 (2016-08-05)
--------------------------

* Bugfix for Django 1.10 compatibility


Version 1.2.3 (2015-12-29)
--------------------------

* Added Django 1.7+ compatible imports for ``get_model()`` and ``get_current_site()``.


Version 1.2.2 (2015-12-28)
--------------------------

* Added Django 1.9 imports for ``ForwardManyToOneDescriptor`` / ``ReverseOneToOneDescriptor``.


Version 1.2.1 (2015-04-16)
--------------------------

* Allow ``is_installed()`` to work before Django app registry is ready.


Version 1.2 (2015-04-16)
------------------------

* Add soft-dependency support for django-any-imagefield_..

Version 1.1.6 (2015-04-16)
--------------------------

* Added ``fluent_utils.softdeps.comments.signals`` stub export.
* Added ``fluent_utils.django_compat.get_meta_model_name()``.
* Added ``fluent_utils.django_compat.is_queryset_empty()``.

Version 1.1.5 (2015-04-08)
--------------------------

* Added new exports in ``fluent_utils.softdeps.comments``: ``get_form()`` and ``signals``


Version 1.1.4 (2015-03-13)
--------------------------

* Fix Django 1.6 compatibility for truncate_name import


Version 1.1.3 (2015-03-13)
--------------------------

* Added ``fluent_utils.django_compat.get_app_label()``
* Added ``fluent_utils.dry.models.get_db_table()``
* Added ``fluent_utils.dry.fields.HideChoicesCharField``


Version 1.1.2 (2015-01-08)
--------------------------

* Fix ``import_apps_submodule()`` and ``import_class()`` to ignore PyDev/PyCharm 4.x import hook.
* Added ``fluent_utils.softdeps.fluent_pages.mixed_reverse_lazy()`` function.


Version 1.1.1 (2014-11-05)
--------------------------

* Fix django-taggit_ support, only django-taggit-autosuggest_ or django-taggit-autocomplete-modified_ worked.


Version 1.1 (2014-10-30)
------------------------

* Add soft-dependency support for django-any-urlfield_.
* ``CommentModelStub``: avoid getting an relation on User and Site


Version 1.0 (2014-09-28)
------------------------

* First release


.. _django-any-urlfield: https://github.com/edoburu/django-any-urlfield
.. _django-any-imagefield: https://github.com/edoburu/django-any-imagefield
.. _django-taggit: https://github.com/alex/django-taggit
.. _django-taggit-autosuggest: https://bitbucket.org/fabian/django-taggit-autosuggest
.. _django-taggit-autocomplete-modified: http://packages.python.org/django-taggit-autocomplete-modified/
.. _taggit-selectize: https://github.com/chhantyal/taggit-selectize

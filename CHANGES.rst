Changelog
=========

Version 1.1.2 (2014-12-11)
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
.. _django-taggit: https://github.com/alex/django-taggit
.. _django-taggit-autosuggest: https://bitbucket.org/fabian/django-taggit-autosuggest
.. _django-taggit-autocomplete-modified: http://packages.python.org/django-taggit-autocomplete-modified/

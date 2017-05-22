from fluent_utils.django_compat import get_app_label, truncate_name


def get_db_table(module, model_name, meta=None, prefix=None):
    """
    Generate a db_table for a model that's being constructed.
    """
    from django.db import connection

    # This function is used in the metaclasses of django-fluent-pages
    # and django-fluent-contents to generate the db_table with a prefix.
    # This duplicates the logic of Django's Options class
    # to make sure the "db_table" is set in advance while creating the class.
    # Setting the db_table afterwards breaks Django 1.7 migrations,
    # which look at Options.original_attrs['db_table'] instead.
    app_label = getattr(meta, 'app_label', None)

    if not app_label:
        # This part differs between Django versions.
        # As of Django 1.7, the app framework is used.
        app_label = get_app_label(module)

    model_name = model_name.lower()
    db_table = "{0}{1}_{2}".format(prefix or '', app_label, model_name)
    return truncate_name(db_table, connection.ops.max_name_length())

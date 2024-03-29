#!/usr/bin/env python
import sys
from os import path

import django
from django.conf import settings
from django.core.management import execute_from_command_line

# Give feedback on used versions
sys.stderr.write("Using Python version {} from {}\n".format(sys.version[:5], sys.executable))
sys.stderr.write(
    "Using Django version {} from {}\n".format(
        django.get_version(), path.dirname(path.abspath(django.__file__))
    )
)

if not settings.configured:
    settings.configure(
        DEBUG=False,  # will be False anyway by DjangoTestRunner.
        DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}},
        INSTALLED_APPS=(
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sites",
            "django.contrib.admin",
            "django.contrib.messages",
            "django.contrib.sessions",
        ),
        MIDDLEWARE=(
            "django.middleware.common.CommonMiddleware",
            "django.contrib.sessions.middleware.SessionMiddleware",
            "django.middleware.csrf.CsrfViewMiddleware",
            "django.contrib.auth.middleware.AuthenticationMiddleware",
            "django.contrib.messages.middleware.MessageMiddleware",
        ),
        SECRET_KEY="testtest",
        TEMPLATES=[
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "DIRS": (),
                "OPTIONS": {
                    "loaders": (
                        "django.template.loaders.filesystem.Loader",
                        "django.template.loaders.app_directories.Loader",
                    ),
                    "context_processors": (
                        "django.template.context_processors.debug",
                        "django.template.context_processors.i18n",
                        "django.template.context_processors.media",
                        "django.template.context_processors.request",
                        "django.template.context_processors.static",
                        "django.contrib.auth.context_processors.auth",
                        "django.contrib.messages.context_processors.messages",
                    ),
                },
            },
        ],
        TEST_RUNNER="django.test.runner.DiscoverRunner",
    )


DEFAULT_TEST_APPS = [
    "fluent_utils",
]


def runtests():
    other_args = list(filter(lambda arg: arg.startswith("-"), sys.argv[1:]))
    test_apps = (
        list(filter(lambda arg: not arg.startswith("-"), sys.argv[1:])) or DEFAULT_TEST_APPS
    )
    argv = sys.argv[:1] + ["test", "--traceback"] + other_args + test_apps
    execute_from_command_line(argv)


if __name__ == "__main__":
    runtests()

#!/usr/bin/env python
import codecs
import re
from os import path

from setuptools import find_packages, setup


def read(*parts):
    file_path = path.join(path.dirname(__file__), *parts)
    return codecs.open(file_path, encoding="utf-8").read()


def find_version(*parts):
    version_file = read(*parts)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return str(version_match.group(1))
    raise RuntimeError("Unable to find version string.")


setup(
    name="django-fluent-utils",
    version=find_version("fluent_utils", "__init__.py"),
    license="Apache 2.0",
    install_requires=[],
    requires=[
        "Django (>=1.4)",
    ],
    description="Internal utilities for code sharing between django-fluent modules",
    long_description=read("README.rst"),
    author="Diederik van der Boor",
    author_email="opensource@edoburu.nl",
    url="https://github.com/edoburu/django-fluent-utils",
    download_url="https://github.com/edoburu/django-fluent-utils/zipball/master",
    packages=find_packages(exclude=("example*",)),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)

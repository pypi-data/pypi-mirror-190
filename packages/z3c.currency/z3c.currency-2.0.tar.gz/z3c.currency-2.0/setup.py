##############################################################################
#
# Copyright (c) 2007 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Setup
"""
import os

from setuptools import find_packages
from setuptools import setup


def read(*rnames):
    with open(os.path.join(os.path.dirname(__file__), *rnames), "rb") as fp:
        return fp.read().decode("utf-8")


tests_require = [
    "z3c.form",
    "zope.testing",
    "zope.testrunner",
]

setup(
    name="z3c.currency",
    version="2.0",
    author="Stephan Richter and the Zope Community",
    author_email="zope-dev@zope.dev",
    description="A currency field and support for ``z3c.form``.",
    long_description=(
        read("README.rst")
        + "\n\n"
        + "Detailed Documentation\n"
        + "**********************\n"
        + "\n"
        + read("src", "z3c", "currency", "README.rst")
        + "\n\n"
        + read("CHANGES.rst")
    ),
    license="ZPL 2.1",
    keywords="zope3 currency schema field widget form",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Zope Public License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP",
        "Framework :: Zope :: 3",
    ],
    url="https://github.com/zopefoundation/z3c.currency",
    packages=find_packages("src"),
    include_package_data=True,
    package_dir={"": "src"},
    namespace_packages=["z3c"],
    python_requires='>=3.7',
    extras_require=dict(
        test=tests_require,
        form=["z3c.form"]),
    install_requires=[
        "setuptools",
        "zope.i18n",
        "zope.i18nmessageid",
        "zope.interface",
        "zope.schema",
    ],
    zip_safe=False,
)

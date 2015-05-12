#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Erigones SDDC API Python Library
#
# Copyright (c) 2015 Erigones, s. r. o.
#
# License: BSD (see LICENSE for details)

import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from erigones_sddc_api import __version__

read = lambda f: open(os.path.join(os.path.dirname(__file__), f)).read()

DEPS = ['requests']

CLASSIFIERS = [
    'Environment :: Web Environment',
    'Environment :: Console',
    'Environment :: Plugins',
    'Intended Audience :: System Administrators',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
    'Development Status :: 5 - Production/Stable',
    'Topic :: Software Development :: Libraries',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

setup(
    name='erigones-sddc-api',
    version=__version__,
    description='Erigones SDDC API Python Library',
    long_description=read('README.rst'),
    url='https://github.com/erigones/erigones-sddc-api/',
    author='Erigones',
    author_email='erigones [at] erigones.com',
    license='BSD',
    packages=('erigones_sddc_api',),
    requires=DEPS,
    platforms='any',
    classifiers=CLASSIFIERS,
    include_package_data=True
)

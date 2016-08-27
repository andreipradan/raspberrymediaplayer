#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import, print_function

from glob import glob
from os.path import basename
from os.path import splitext

from setuptools import find_packages
from setuptools import setup


install_requires = [
    'Django>=1.10, <1.11',
    'djangorestframework',
    'django-heartbeat==2.0.2',
    'django-bootstrap3',
    'youtube-dl'
]

setup(
    name='raspberrymediaplayer',
    version='1.0.0',
    description=(
        'Django powered website for playing media like mp3 files, radio live '
        'streams or even youtube songs on the raspberry pi (or any unix based '
        'computer)'
    ),
    author='Andrei Pradan',
    author_email='andrei.pradan@gmail.com',
    url='',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
)

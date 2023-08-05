#!/usr/bin/env python

import sys

from setuptools import setup

with open('README.rst', 'r') as readme:
    long_description = readme.read()

setup(
    name='django-cust-email-user',
    version='0.1.2',
    author='red-pepper-services',
    author_email='pypi@schiegg.at',
    url='https://github.com/red-pepper-services/django-emailuser',
    license='MIT',
    description="Just another Django-email-user app. Makes the email address as the username.",
    long_description=long_description,
    include_package_data=True,
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
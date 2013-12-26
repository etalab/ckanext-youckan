#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

from os.path import join

from setuptools import setup, find_packages

from ckanext.youckan import __version__, __description__

RE_REQUIREMENT = re.compile(r'^\s*-r\s*(?P<filename>.*)$')

PYPI_RST_FILTERS = (
    # Remove travis ci badge
    (r'.*travis-ci\.org/.*', ''),
    # Remove pypip.in badges
    (r'.*pypip\.in/.*', ''),
    (r'.*crate\.io/.*', ''),
    (r'.*coveralls\.io/.*', ''),
)


def rst(filename):
    '''
    Load rst file and sanitize it for PyPI.
    Remove unsupported github tags:
     - code-block directive
     - travis ci build badge
    '''
    content = open(filename).read()
    for regex, replacement in PYPI_RST_FILTERS:
        content = re.sub(regex, replacement, content)
    return content


def pip(filename):
    '''Parse pip requirement file and transform it to setuptools requirements'''
    requirements = []
    for line in open(join('requirements', filename)).readlines():
        line = line.split('#')[0].strip()  # Remove comments
        if not line:
            continue
        match = RE_REQUIREMENT.match(line)
        if match:
            requirements.extend(pip(match.group('filename')))
        elif not line.startswith('-e'):
            requirements.append(line)
    return requirements


long_description = '\n'.join((
    rst('README.rst'),
    rst('CHANGELOG.rst'),
    ''
))

setup(
    name='ckanext-youckan',
    version=__version__,
    description=__description__,
    long_description=long_description,
    keywords='CKAN, OAuth2, YouCKAN',
    author='Axel Haustant',
    author_email='axel.haustant@etalab2.fr',
    url='https://github.com/etalab/ckanext-youckan',
    license='',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=['ckanext'],
    include_package_data=True,
    zip_safe=False,
    install_requires=pip('install.pip'),
    entry_points={
        'ckan.plugins': [
            'youckan = ckanext.youckan.plugins:YouckanPlugin',
            'sentry = ckanext.youckan.plugins:SentryPlugin',
        ]
    },
    extras_require={
        'test': pip('test.pip'),
        'sentry': pip('sentry.pip'),
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        'Framework :: Pylons',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Session',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Systems Administration :: Authentication/Directory',
    ],
)

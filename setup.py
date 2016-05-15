# -*- coding: utf-8 -*-
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': "Parse Ruby's Gemfiles",
    'author': 'Balasankar C',
    'url': 'https://gitlab.com/balasankarc/gemfileparser',
    'download_url': 'https://gitlab.com/balasankarc/gemfileparser',
    'author_email': 'balasankarc@autistici.org',
    'version': '0.5',
    'license': 'GPL-3+',
    'long_description': '''
Installation
~~~~~~~~~~~~

| If using pip, use the command ``sudo pip install gemfileparser``
| Else use the following commands

::

    git clone https://github.com/balasankarc/gemfileparser.git
    cd gemfileparser
    python setup.py install

Usage
~~~~~

::

    from gemfileparser import gemfileparser
    parser = gemfileparser.GemfileParser(<path to Gemfile>, <name of the application (optional)>)
    dependency_dictionary = parser.parse()

The parse() method returns a dict object of the following format

::

    {
    'development': [list of dependency objects inside group 'development'],
    'runtime': [list of runtime dependency objects],
    .
    .
    .}

Each dependency object contains the following attributes

::

    name - Name of the gem
    requirement - Version requirement
    autorequire - Autorequire value
    source - Source URL of the gem
    parent - Dependency of which gem
    group - Group in which gem is a member of (default : runtime)

Example
^^^^^^^

::

    from gemfileparser import gemfileparser
    n = gemfileparser.GemfileParser('Gemfile', 'diaspora')
    deps = n.parse()
    for key in deps:
       if deps[key]:
           print key
           for dependency in deps[key]:
               print "\t", dependency

Copyright
~~~~~~~~~

2015 Balasankar C balasankarc@autistici.org

License
~~~~~~~

gemfileparser is released under `GNU GPL version 3 (or above) License`_.

.. _GNU GPL version 3 (or above) License: http://www.gnu.org/licenses/gpl
''',
    'install_requires': ['nose'],
    'packages': ['gemfileparser'],
    'scripts': [],
    'name': 'gemfileparser'
}

setup(
    classifiers=[
        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
    ], **config)

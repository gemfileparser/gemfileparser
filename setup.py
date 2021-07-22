# -*- coding: utf-8 -*-

from setuptools import setup


setup(
    entry_points={
        'console_scripts': [
            'parsegemfile = gemfileparser:command_line',
        ],
    },
)
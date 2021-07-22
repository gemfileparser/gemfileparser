#!/usr/bin/env python
#
# Copyright (c) Balasankar C <balasankarc@autistici.org> and others
# SPDX-License-Identifier: GPL-3.0-or-later OR MIT

from gemfileparser import GemfileParser


def check_gemparser_results(test_file, regen=False):
    """
    Run GemfileParser.parse on `test_file` and check against a JSON file that
    contains expected results with the same name as the `test_file` with a
    "-expected.json" suffix appended.
    """
    import json

    gemparser = GemfileParser(test_file)
    dependencies = {
        group: [dep.to_dict() for dep in deps]
            for group, deps in gemparser.parse().items()
    }

    expected_file = test_file + '-expected.json'
    if regen:
        with open(expected_file, 'w') as o:
            json.dump(dependencies, o, indent=2)

    with open(expected_file) as o:
        expected = json.load(o)

    assert expected == dependencies


def test_source_only_gemfile():
    check_gemparser_results('tests/Gemfile')


def test_gemfile_1():
    check_gemparser_results('tests/Gemfile_1')


def test_gemfile_2():
    check_gemparser_results('tests/Gemfile_2')


def test_gemfile_3():
    check_gemparser_results('tests/Gemfile_3')


def test_gemfile_4():
    check_gemparser_results('tests/Gemfile_4')


def test_gemfile_platforms():
    check_gemparser_results('tests/Gemfile_5')


def test_gemspec_1():
    check_gemparser_results('tests/sample.gemspec')


def test_gemspec_2():
    check_gemparser_results('tests/address_standardization.gemspec')


def test_gemspec_3():
    check_gemparser_results('tests/arel.gemspec')

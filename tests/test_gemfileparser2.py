#!/usr/bin/env python
#
# Copyright (c) Balasankar C <balasankarc@autistici.org> and others
# SPDX-License-Identifier: GPL-3.0-or-later OR MIT

import os

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')


def check_gemparser_results(test_file, regen=False):
    """
    Run GemfileParser.parse on ``test_file`` and check against a JSON file that
    contains expected results with the same name as the ``test_file`` with a
    "-expected.json" suffix appended.
    """
    test_file = os.path.join(TEST_DATA_DIR, test_file)

    from gemfileparser2 import GemfileParser as GemfileParser2
    from gemfileparser import GemfileParser
    _check_gemparser_results(test_file, parser=GemfileParser, regen=regen)
    _check_gemparser_results(test_file, parser=GemfileParser2, regen=regen)


def _check_gemparser_results(test_file, parser, regen=False):
    import json
    gemparser = parser(test_file)
    dependencies = {
        group: [dep.to_dict() for dep in deps]
        for group, deps in gemparser.parse().items()
    }

    expected_file = f"{test_file}-expected.json"
    if regen:
        with open(expected_file, "w") as o:
            json.dump(dependencies, o, indent=2)

    with open(expected_file) as o:
        expected = json.load(o)

    assert dependencies == expected


def test_source_only_gemfile():
    check_gemparser_results("gemfiles/Gemfile")


def test_gemfile_1():
    check_gemparser_results("gemfiles/Gemfile_1")


def test_gemfile_2():
    check_gemparser_results("gemfiles/Gemfile_2")


def test_gemfile_3():
    check_gemparser_results("gemfiles/Gemfile_3")


def test_gemfile_4():
    check_gemparser_results("gemfiles/Gemfile_4")


def test_gemfile_platforms():
    check_gemparser_results("gemfiles/Gemfile_5")


def test_gemspec_1():
    check_gemparser_results("gemspecs/sample.gemspec")


def test_gemspec_2():
    check_gemparser_results("gemspecs/address_standardization.gemspec")


def test_gemspec_3():
    check_gemparser_results("gemspecs/arel.gemspec")


def test_gemspec_no_deps():
    check_gemparser_results("gemspecs/arel2.gemspec", regen=False)


def test_gemspec_4():
    check_gemparser_results("gemspecs/logstash-mixin-ecs_compatibility_support.gemspec")

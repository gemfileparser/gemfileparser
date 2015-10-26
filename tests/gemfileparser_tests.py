#!/usr/bin/env python

from nose.tools import assert_equal
from gemfileparser import gemfileparser


def test_source_only_gemfile():
    gemparser = gemfileparser.GemfileParser('tests/Gemfile')
    expected = {'development': [], 'production': [], 'runtime': [], 'test': []}
    dependencies = gemparser.parse()
    assert_equal(dependencies, expected)


def test_name():
    gemparser = gemfileparser.GemfileParser('tests/Gemfile_2')
    dependencies = gemparser.parse()
    assert_equal(dependencies['runtime'][0].name, 'rails')


def test_requirement():
    gemparser = gemfileparser.GemfileParser('tests/Gemfile_2')
    dependencies = gemparser.parse()
    assert_equal(dependencies['runtime'][0].requirement, '4.2.4')


def test_group():
    gemparser = gemfileparser.GemfileParser('tests/Gemfile_3')
    dependencies = gemparser.parse()
    assert_equal(dependencies['development'][0].requirement, '4.2.4')


def test_group_block():
    gemparser = gemfileparser.GemfileParser('tests/Gemfile_2')
    dependencies = gemparser.parse()
    assert_equal(dependencies['development'][0].requirement, '3.0.0')
    assert_equal(dependencies['runtime'][0].requirement, '4.2.4')


def test_source():
    gemparser = gemfileparser.GemfileParser('tests/Gemfile_2')
    dependencies = gemparser.parse()
    assert_equal(dependencies['runtime'][0].source,
                 'http://www.example.com')

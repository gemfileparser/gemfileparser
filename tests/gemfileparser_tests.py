#!/usr/bin/env python

from nose.tools import assert_equal, assert_in
from gemfileparser import GemfileParser


def test_source_only_gemfile():
    gemparser = GemfileParser('tests/Gemfile')
    expected = {
        'development': [],
        'test': [],
        'runtime': [],
        'metrics': [],
        'production': []}
    dependencies = gemparser.parse()
    assert_equal(dependencies, expected)


def test_name():
    gemparser = GemfileParser('tests/Gemfile_2')
    dependencies = gemparser.parse()
    assert_equal(dependencies['runtime'][0].name, 'rails')


def test_requirement():
    gemparser = GemfileParser('tests/Gemfile_2')
    dependencies = gemparser.parse()
    assert_equal(dependencies['runtime'][0].requirement, '4.2.4')


def test_group():
    gemparser = GemfileParser('tests/Gemfile_3')
    dependencies = gemparser.parse()
    assert_equal(dependencies['development'][0].requirement, '4.2.4')


def test_group_block():
    gemparser = GemfileParser('tests/Gemfile_2')
    dependencies = gemparser.parse()
    assert_equal(dependencies['development'][0].requirement, '3.0.0')
    assert_equal(dependencies['runtime'][0].requirement, '4.2.4')


def test_source():
    gemparser = GemfileParser('tests/Gemfile_2')
    dependencies = gemparser.parse()
    assert_equal(dependencies['runtime'][0].source,
                 'http://www.example.com')


def test_gemspec():
    gemparser = GemfileParser('tests/Gemfile_2')
    dependencies = gemparser.parse()
    assert_in('rails', [x.name for x in dependencies['runtime']])
    assert_in('responders', [x.name for x in dependencies['development']])

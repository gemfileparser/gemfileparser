#!/usr/bin/env python
#
# Copyright (c) Balasankar C <balasankarc@autistici.org>

# gemfileparser is dual-licensed under [GNU GPL version 3 (or above) License]
# (http://www.gnu.org/licenses/gpl)
# and [MIT License](https://opensource.org/licenses/MIT).

# Personally, I prefer anyone using this to respect the GPL license and use that
# itself for derivative works - thus making them also Free Software. But, your
# call.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# .
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# .
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# MIT License
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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

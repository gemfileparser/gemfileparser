#!/usr/bin/env python
#
# Copyright 2015 Balasankar C <balasankarc@autistici.org>

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


def test_source_only_gemfile():
    gemparser = GemfileParser('tests/Gemfile')
    expected = {
        'dependency': [],
        'development': [],
        'test': [],
        'metrics': [],
        'runtime': [],
        'production': [],
    }
    dependencies = gemparser.parse()
    assert expected == dependencies


def test_name():
    gemparser = GemfileParser('tests/Gemfile_2')
    dependencies = gemparser.parse()
    assert 'rails' == dependencies['runtime'][0].name


def test_requirement():
    gemparser = GemfileParser('tests/Gemfile_2')
    dependencies = gemparser.parse()
    assert ['4.2.4'] == dependencies['runtime'][0].requirement


def test_group():
    gemparser = GemfileParser('tests/Gemfile_3')
    dependencies = gemparser.parse()
    assert ['4.2.4'] == dependencies['development'][0].requirement


def test_group_block():
    gemparser = GemfileParser('tests/Gemfile_2')
    dependencies = gemparser.parse()
    assert ['3.0.0'] == dependencies['development'][0].requirement
    assert ['4.2.4'] == dependencies['runtime'][0].requirement


def test_source():
    gemparser = GemfileParser('tests/Gemfile_2')
    dependencies = gemparser.parse()
    assert 'http://www.example.com' == dependencies['runtime'][0].source


def test_gemspec():
    gemparser = GemfileParser('tests/Gemfile_2')
    dependencies = gemparser.parse()
    assert 'rails' in [x.name for x in dependencies['runtime']]
    assert 'responders' in [x.name for x in dependencies['development']]

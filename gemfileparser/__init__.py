#!/usr/bin/env python
#
# Copyright (c) Balasankar C <balasankarc@autistici.org> and others

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
#
#
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

'''Python library to parse Ruby's Gemfiles and gemspec files.'''

import collections
import csv
import glob
import io
import os
import re


class Dependency(object):
    ''' A class to hold information about a dependency gem.'''

    def __init__(self):
        self.name = ''
        self.requirement = []
        self.autorequire = ''
        self.source = ''
        self.parent = []
        self.group = ''

    def to_dict(self):
        return dict(
            name=self.name,
            requirement=self.requirement,
            autorequire=self.autorequire,
            source=self.source,
            parent=self.parent,
            group=self.group,
        )


class GemfileParser(object):
    '''Creates a GemfileParser object to perform operations. '''

    gemfile_regexes = collections.OrderedDict()
    gemfile_regexes['source'] = re.compile(
        r"source:[ ]?(?P<source>[a-zA-Z:\/\.-]+)")
    gemfile_regexes['git'] = re.compile(
        r"git:[ ]?(?P<git>[a-zA-Z:\/\.-]+)")
    gemfile_regexes['platform'] = re.compile(
        r"platform:[ ]?(?P<platform>[a-zA-Z:\/\.-]+)")
    gemfile_regexes['path'] = re.compile(
        r"path:[ ]?(?P<path>[a-zA-Z:\/\.-]+)")
    gemfile_regexes['branch'] = re.compile(
        r"branch:[ ]?(?P<branch>[a-zA-Z:\/\.-]+)")
    gemfile_regexes['autorequire'] = re.compile(
        r"require:[ ]?(?P<autorequire>[a-zA-Z:\/\.-]+)")
    gemfile_regexes['group'] = re.compile(
        r"group:[ ]?(?P<group>[a-zA-Z:\/\.-]+)")
    gemfile_regexes['name'] = re.compile(
        r"(?P<name>[a-zA-Z]+[\.0-9a-zA-Z _-]*)")
    gemfile_regexes['requirement'] = re.compile(
        r"(?P<requirement>([>|<|=|~>|\d]+[ ]*[0-9\.\w]+[ ,]*)+)")

    group_block_regex = re.compile(
        r"group[ ]?:[ ]?(?P<groupblock>.*?) do")
    add_dvtdep_regex = re.compile(
        r".*add_development_dependency(?P<line>.*)")
    add_rundep_regex = re.compile(
        r".*add_runtime_dependency(?P<line>.*)")
    add_dep_regex = re.compile(
        r".*dependency(?P<line>.*)")

    def __init__(self, filepath, appname=''):
        self.filepath = filepath  # Required when calls to gemspec occurs

        self.current_group = 'runtime'

        self.appname = appname
        self.dependencies = {
            'development': [],
            'runtime': [],
            'dependency': [],
            'test': [],
            'production': [],
            'metrics': [],
        }
        with open(filepath) as gf:
            self.contents = gf.readlines()

        if filepath.endswith(('.gemspec', '.podspec')):
            self.gemspec = True
        else:
            self.gemspec = False

    @staticmethod
    def preprocess(line):
        '''Removes the comment portion and excess spaces.'''

        if "#" in line:
            line = line[:line.index('#')]
        line = line.strip()
        return line

    def parse_line(self, line):
        '''Parses each line and creates dependency objects accordingly'''

        try:

            # StringIO requires a unicode object.
            # But unicode() doesn't work with Python3
            # as it is already in unicode format.
            # So, first try converting and if that fails, use original.

            line = unicode(line)
        except NameError:
            pass
        linefile = io.StringIO(line)  # csv requires a file object
        for line in csv.reader(linefile, delimiter=','):
            column_list = []
            for column in line:
                stripped_column = column.replace("'", "")
                stripped_column = stripped_column.replace('"', "")
                stripped_column = stripped_column.replace("%q<", "")
                stripped_column = stripped_column.replace("(", "")
                stripped_column = stripped_column.replace(")", "")
                stripped_column = stripped_column.replace("[", "")
                stripped_column = stripped_column.replace("]", "")
                stripped_column = stripped_column.strip()
                column_list.append(stripped_column)
            dep = Dependency()
            dep.group = self.current_group
            dep.parent.append(self.appname)
            for column in column_list:
                # Check for a match in each regex and assign to
                # corresponding variables
                for criteria in GemfileParser.gemfile_regexes:
                    criteria_regex = GemfileParser.gemfile_regexes[criteria]
                    match = criteria_regex.match(column)
                    if match:
                        if criteria == 'requirement':
                            dep.requirement.append(match.group(criteria))
                        else:
                            setattr(dep, criteria, match.group(criteria))
                        break
            if dep.group in self.dependencies:
                self.dependencies[dep.group].append(dep)
            else:
                self.dependencies[dep.group] = [dep]

    def parse_gemfile(self, path=''):
        '''Parses a Gemfile and returns a dict of categorized dependencies.'''

        if path == '':
            contents = self.contents
        else:
            contents = open(path).readlines()
        for line in contents:
            line = self.preprocess(line)
            if line == '' or line.startswith('source'):
                continue
            elif line.startswith('group'):
                match = self.group_block_regex.match(line)
                if match:
                    self.current_group = match.group('groupblock')
            elif line.startswith('end'):
                self.current_group = 'runtime'
            elif line.startswith('gemspec'):
                # Gemfile contains a call to gemspec
                gemfiledir = os.path.dirname(self.filepath)
                gemspec_list = glob.glob(os.path.join(gemfiledir, "*.gemspec"))
                if len(gemspec_list) > 1:
                    print("Multiple gemspec files found")
                    continue
                gemspec_file = gemspec_list[0]
                self.parse_gemspec(path=os.path.join(gemfiledir, gemspec_file))
            elif line.startswith('gem '):
                line = line[3:]
                self.parse_line(line)
        return self.dependencies

    def parse_gemspec(self, path=''):
        '''Method to handle gemspec files.'''

        if path == '':
            contents = self.contents
        else:
            contents = open(path).readlines()
        for line in contents:
            line = self.preprocess(line)
            match = GemfileParser.add_dvtdep_regex.match(line)
            if match:
                self.current_group = 'development'
            else:
                match = GemfileParser.add_rundep_regex.match(line)
                if match:
                    self.current_group = 'runtime'
                else:
                    match = GemfileParser.add_dep_regex.match(line)
                    if match:
                        self.current_group = 'dependency'
            if match:
                line = match.group('line')
                self.parse_line(line)
        return self.dependencies

    def parse(self):
        '''Calls necessary function based on whether file is a gemspec file
        or not and forwards the dicts returned by them.'''
        if self.gemspec:
            return self.parse_gemspec()
        else:
            return self.parse_gemfile()


def command_line():
    """
    A minimal command line entry point.
    """
    import sys
    if len(sys.argv) < 2:
        print("Usage : parsegemfile <input file>")
        sys.exit(0)

    parsed = GemfileParser(sys.argv[1])
    output = parsed.parse()
    for key, value in list(output.items()):
        print(key, ":")
        for item in value:
            print("\t", item)

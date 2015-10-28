#!/usr/bin/env python
#
# Copyright 2015 Balasankar C <balasankarc@autistici.org>
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

import csv
import io
import re
import os
import glob


class GemfileParser:

    gemname_regex = re.compile(r"(?P<gemname>[a-zA-Z]+[0-9a-zA-Z _-]*)")
    req_regex = re.compile(r"(?P<reqs>([>|<|=|~>|\d]+[ ]*[0-9\.\w]+[ ,]*)+)")
    source_regex = re.compile(r"source:[ ]?(?P<source>[a-zA-Z:\/\.-]+)")
    autoreq_regex = re.compile(r"require:[ ]?(?P<autoreq>[a-zA-Z:\/\.-]+)")
    group_regex = re.compile(r"group:[ ]?(?P<groupname>[a-zA-Z:\/\.-]+)")
    group_block_regex = re.compile(r"group[ ]?:[ ]?(?P<groupblock>.*?) do")
    add_dvtdep_regex = re.compile(r".*add_development_dependency (?P<line>.*)")
    add_rundep_regex = re.compile(r".*add_runtime_dependency (?P<line>.*)")

    GROUP = 'runtime'

    class Dependency:
        ''' A class to hold information about a dependency gem.'''

        def __init__(self):
            self.name = ''
            self.requirement = ''
            self.autorequire = ''
            self.source = ''
            self.parent = ''
            self.group = ''

        def __str__(self):
            return self.name + ", " + self.requirement

    def __init__(self, filepath, appname=''):
        self.filepath = filepath    # Required when calls to gemspec occurs
        self.gemfile = open(filepath)
        self.appname = appname
        self.dependencies = {
                                'development': [],
                                'runtime': [],
                                'test': [],
                                'production': []
                            }
        self.contents = self.gemfile.readlines()
        if filepath.endswith('gemspec'):
            self.gemspec = True
        else:
            self.gemspec = False

    def preprocess(self, line):
        if "#" in line:
            line = line[:line.index('#')]
        line = line.strip()
        return line

    def parse_line(self, line):
        try:

            # StringIO requires a unicode object.
            # But unicode() doesn't work with Python3
            # as it is already in unicode format.
            # So, first try converting and if that fails, use original.

            line = unicode(line)
        except:
            pass
        linefile = io.StringIO(line)    # csv requires a file object
        for line in csv.reader(linefile, delimiter=','):
            column_list = []
            for column in line:
                stripped_column = column.replace("'", "")
                stripped_column = stripped_column.replace('"', "")
                stripped_column = stripped_column.strip()
                column_list.append(stripped_column)
            dep = self.Dependency()
            dep.group = self.GROUP
            dep.parent = self.appname
            for column in column_list:
                # Check for a match in each regex and assign to
                # corresponding variables
                match = self.source_regex.match(column)
                if match:
                    dep.source = match.group('source')
                    continue
                match = self.group_regex.match(column)
                if match:
                    dep.group = match.group('groupname')
                    continue
                match = self.autoreq_regex.match(column)
                if match:
                    dep.autorequire = match.group('autoreq')
                    continue
                match = self.gemname_regex.match(column)
                if match:
                    dep.name = match.group('gemname')
                    continue
                match = self.req_regex.match(column)
                if match:
                    if dep.requirement == '':
                        dep.requirement = match.group('reqs')
                    else:
                        dep.requirement += ' ' + match.group('reqs')
                    continue
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
                    self.GROUP = match.group('groupblock')
            elif line.startswith('end'):
                self.GROUP = 'runtime'
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
        if path == '':
            contents = self.contents
        else:
            contents = open(path).readlines()
        for line in contents:
            line = self.preprocess(line)
            match = self.add_dvtdep_regex.match(line)
            if match:
                self.GROUP = 'development'
            else:
                match = self.add_rundep_regex.match(line)
                if match:
                    self.GROUP = 'runtime'
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

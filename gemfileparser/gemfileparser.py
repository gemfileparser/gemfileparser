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

    def parse_gemfile(self, path=''):
        if path == '':
            contents = self.contents
        else:
            contents = open(path).readlines()
        for line in contents:
            line = line.strip()
            if line.startswith('source') or line.startswith('#'):
                continue
            elif line.startswith('group'):
                match = self.group_block_regex.match(line)
                if match:
                    self.GROUP = match.group('groupblock')
            elif line.startswith('end'):
                self.GROUP = 'runtime'
            elif line.startswith('gemspec'):
                print 'gemspec'
                self.parse_gemspec(path='sample.gemspec')
                print self.dependencies
            elif line.startswith('gem'):
                line = unicode(line[3:])
                linefile = io.StringIO(line)
                for line in csv.reader(linefile, delimiter=','):
                    column_list = []
                    for column in line:
                        stripped_column = column.replace("'", "")
                        stripped_column = stripped_column.replace('"', "")
                        stripped_column = stripped_column.strip()
                        if "#" in stripped_column:
                            pos = stripped_column.index("#")
                            stripped_column = stripped_column[:pos]
                        column_list.append(stripped_column)
                    dep = self.Dependency()
                    dep.group = self.GROUP
                    dep.parent = self.appname
                    for column in column_list:
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
        return self.dependencies

    def parse_gemspec(self, path=''):
        if path == '':
            contents = self.contents
        else:
            contents = open(path).readlines()
        for line in contents:
            line = line.strip()
            print line
            match = self.add_dvtdep_regex.match(line)
            if match:
                self.GROUP = 'development'
            else:
                match = self.add_rundep_regex.match(line)
                if match:
                    self.GROUP = 'runtime'
            if match:
                line = unicode(match.group('line'))
                linefile = io.StringIO(line)
                for line in csv.reader(linefile, delimiter=','):
                    column_list = []
                    for column in line:
                        stripped_column = column.replace("'", "")
                        stripped_column = stripped_column.replace('"', "")
                        stripped_column = stripped_column.strip()
                        if "#" in stripped_column:
                            pos = stripped_column.index("#")
                            stripped_column = stripped_column[:pos]
                        column_list.append(stripped_column)
                    dep = self.Dependency()
                    dep.group = self.GROUP
                    dep.parent = self.appname
                    for column in column_list:
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
        return self.dependencies

    def parse(self):
        ''' Returns a dictionary of dependency objects categorized under
        groups.'''
        if self.gemspec:
            return self.parse_gemspec()
        else:
            return self.parse_gemfile()

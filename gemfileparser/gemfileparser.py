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
import StringIO
import re


class GemfileParser:

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

    gemname_regex = re.compile(r"(?P<gemname>[a-zA-Z]+[0-9a-zA-Z _-]*)")
    req_regex = re.compile(r"(?P<reqs>([>|<|=|~>|\d]+[ ]*[0-9\.\w]+[ ,]*)+)")
    source_regex = re.compile(r"source:[ ]?(?P<source>[a-zA-Z:\/\.-]+)")
    autoreq_regex = re.compile(r"require:[ ]?(?P<autoreq>[a-zA-Z:\/\.-]+)")
    group_regex = re.compile(r"group:[ ]?(?P<groupname>[a-zA-Z:\/\.-]+)")
    group_block_regex = re.compile(r"group[ ]?:[ ]?(?P<groupblock>.*) do")

    def __init__(self, filepath):
        self.gemfile = open(filepath)
        self.dependencies = {'development': [],
                             'runtime': [], 'test': [], 'production': []}
        self.contents = self.gemfile.readlines()
        if filepath.endswith('gemspec'):
            self.gemspec = True
        else:
            self.gemspec = False

    def parse(self):
        for line in self.contents:
            line = line.strip()
            if line.startswith('source') or line.startswith('#'):
                continue
            elif line.startswith('group'):
                match = self.group_block_regex.match(line)
                if match:
                    self.GROUP = match.group('groupblock')
            elif line.startswith('end'):
                self.GROUP = 'runtime'
            elif line.startswith('gem'):
                line = line[3:]
                linefile = StringIO.StringIO(line)
                for i in csv.reader(linefile, delimiter=','):
                    m = []
                    for k in i:
                        l = k.replace("'", "").replace('"', "").strip()
                        if "#" in l:
                            l = l[:l.index("#")]
                        m.append(l)
                    dep = self.Dependency()
                    dep.group = self.GROUP
                    for k in m:
                        match = self.source_regex.match(k)
                        if match:
                            dep.source = match.group('source')
                            continue
                        match = self.group_regex.match(k)
                        if match:
                            dep.group = match.group('groupname')
                            continue
                        match = self.autoreq_regex.match(k)
                        if match:
                            dep.autorequire = match.group('autoreq')
                            continue
                        match = self.gemname_regex.match(k)
                        if match:
                            dep.name = match.group('gemname')
                            continue
                        match = self.req_regex.match(k)
                        if match:
                            if dep.requirement == '':
                                dep.requirement = match.group('reqs')
                            else:
                                dep.requirement += ' ' + match.group('reqs')
                            continue
                    dep.parent = 'diaspora'
                    if self.GROUP in self.dependencies:
                        self.dependencies[self.GROUP].append(dep)
                    else:
                        self.dependencies[self.GROUP] = [dep]
        return self.dependencies

if __name__ == "__main__":
    n = GemfileParser('Gemfile')
    deps = n.parse()
    for key in deps:
        print key
        for dependency in deps[key]:
            print "\t", dependency

# gemfileparser
Parse Ruby Gemfile's using Python. Supports Gemfiles and .gemspec files.

### Installation
If using pip, use the command `sudo pip install gemfileparser`  
Else use the following commands
```
git clone https://github.com/balasankarc/gemfileparser.git
cd gemfileparser
python setup.py install
```

### Usage
```
from gemfileparser import GemfileParser
parser = GemfileParser(<path to Gemfile>, <name of the application (optional)>)
dependency_dictionary = parser.parse()
```
The parse() method returns a dict object of the following format
```
{
'development': [list of dependency objects inside group 'development'],
'runtime': [list of runtime dependency objects],
.
.
.}
```
Each dependency object contains the following attributes
```
name - Name of the gem
requirement - Version requirement
autorequire - Autorequire value
source - Source URL of the gem
parent - Dependency of which gem
group - Group in which gem is a member of (default : runtime)
```

#### Example
```
from gemfileparser import GemfileParser
n = GemfileParser('Gemfile', 'diaspora')
deps = n.parse()
for key in deps:
   if deps[key]:
       print key
       for dependency in deps[key]:
           print "\t", dependency
```

### Copyright
2020 Gemfileparser authors (listed in AUTHORS file)
2015-2018 Balasankar C <balasankarc@autistici.org>

### License

gemfileparser is dual-licensed under [GNU GPL version 3 (or above) License](http://www.gnu.org/licenses/gpl)
and [MIT License](https://opensource.org/licenses/MIT).

It is preferred anyone using this project to respect the GPL-3+ license and use
that itself for derivative works - thus making them also Free Software. But,
your call.

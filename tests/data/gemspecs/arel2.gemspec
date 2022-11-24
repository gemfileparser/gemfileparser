# -*- encoding: utf-8 -*-

Gem::Specification.new do |s|
  s.name = arel2
  s.version = "2.0.7.beta.20110429111451"

  s.required_rubygems_version = Gem::Requirement.new("> 1.3.1") if s.respond_to? :required_rubygems_version=
  s.authors = ["Aaron Patterson", "Bryan Halmkamp", "Emilio Tagua", "Nick Kallen"]
  s.date = %q{2011-04-29}
  s.description = %q{Arel is a SQL AST manager for Ruby.}
  s.email = ["aaron@tenderlovemaking.com", "bryan@brynary.com", "miloops@gmail.com", "nick@example.org"]
  s.extra_rdoc_files = ["History.txt", "MIT-LICENSE.txt", "Manifest.txt", "README.markdown"]
  s.files = [".autotest", ".gemtest", "History.txt", "MIT-LICENSE.txt"]
  s.homepage = %q{http://github.com/rails/arel}
  s.rdoc_options = ["--main", "README.markdown"]
  s.require_paths = ["lib"]
  s.rubyforge_project = %q{arel}
  s.rubygems_version = %q{1.6.1}
  s.summary = %q{Arel is a SQL AST manager for Ruby}
  s.test_files = ["test/attributes/test_attribute.rb", "test/nodes/test_as.rb"]

end

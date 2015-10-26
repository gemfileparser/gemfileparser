try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': "Parse Ruby's Gemfiles",
    'author': 'Balasankar C',
    'url': 'https://gitlab.com/balasankarc/gemfileparser',
    'download_url': 'https://gitlab.com/balasankarc/gemfileparser',
    'author_email': 'balasankarc@autistici.org',
    'version': '0.2',
    'install_requires': ['nose', 'csv'],
    'packages': ['gemfileparser'],
    'scripts': [],
    'name': 'gemfileparser'
}

setup(**config)

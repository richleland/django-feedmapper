import os
import sys
from setuptools import setup, find_packages

def read_file(filename):
    """Read a file into a string"""
    path = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(path, filename)
    try:
        return open(filepath).read()
    except IOError:
        return ''

def get_readme():
    """Return the README file contents. Supports text ,rst, and markdown"""
    for name in ('README','README.rst','README.md'):
        if os.path.exists(name):
            return read_file(name)
    return ''

# Use the docstring of the __init__ file to be the description
__import__('feedmapper')
DESC = " ".join(sys.modules['feedmapper'].__doc__.splitlines()).strip()

setup(
    name = "django-feedmapper",
    version = sys.modules['feedmapper'].get_version().replace(' ', '-'),
    url = 'https://github.com/natgeo/django-feedmapper',
    license= 'BSD',
    author = 'National Geographic',
    author_email = 'appdev@ngs.org',
    description = DESC,
    long_description = get_readme(),
    packages = find_packages(),
    namespace_packages=[],
    include_package_data = True,
    install_requires = read_file('requirements.txt'),
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
)


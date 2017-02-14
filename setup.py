import sys
import os

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to pytest")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ['tests']

    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


here = os.path.abspath(os.path.dirname(__file__))

version_file = open(os.path.join(here, 'jsub', 'VERSION'))
version = version_file.read().strip()

with open(os.path.join(here, 'README.rst')) as f:
    long_description = f.read()

setup(
    name = 'jsub',
    version = version,
    description = 'Job submission toolkit bundle',
    long_description = long_description,
    url = 'https://jsubpy.github.io/',
    author = 'Xianghu Zhao',
    author_email = 'zhaoxh@ihep.ac.cn',
    license = 'MIT',

    classifiers = [
        'Development Status :: 2 - Pre-Alpha',

        'Intended Audience :: Science/Research',
        'Topic :: System :: Distributed Computing',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords = 'Job submission tools',
    packages = find_packages(exclude=[]),
    install_requires = [
        'click',
        'PyYAML',
        'pytoml',
    ],
    include_package_data = True,
    tests_require = [
        'pytest',
    ],
    entry_points = {
        'console_scripts': [
            'jsub = jsub.command:main',
        ],
    },
    cmdclass = {'test': PyTest},
)

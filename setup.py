import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

from jsub import Jsub

class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to pytest")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ['tests']

    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)

setup(
    name = 'jsub',
    version = Jsub().version(),
    description = 'Job submission toolkit',
    packages = find_packages(),
    install_requires = [
        'click',
        'PyYAML',
        'pytoml',
    ],
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

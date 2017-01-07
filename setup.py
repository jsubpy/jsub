import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

from jsub.version import jsub_version

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
    version = jsub_version(),
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
            'jsub = jsub.run:main',
        ],
    },
    cmdclass = {'test': PyTest},
)

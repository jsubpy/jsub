from setuptools import setup, find_packages

import jsub

setup(
    name = 'jsub',
    version = jsub.version(),
    description = 'Job submission toolkit',
    packages = find_packages(),
    install_requires = [
        'click',
    ],
    entry_points = {
        'console_scripts': [
            'jsub = jsub.run:main',
        ],
    },
)

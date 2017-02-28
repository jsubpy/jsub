#!/bin/sh

cd $(dirname $0)

python -m pytest -s tests
#python setup.py test

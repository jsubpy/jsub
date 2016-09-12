#!/bin/sh

cd $(dirname $0)

python -m pytest tests
#python setup.py test

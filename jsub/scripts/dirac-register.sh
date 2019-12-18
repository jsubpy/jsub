#!/bin/sh

if [ -z "$DIRAC" ]; then
  >&2 echo 'DIRAC environment is not set'
  exit 1
fi

source "$DIRAC/bashrc"

cur_dir=$(dirname $0)

"$cur_dir/dirac-register.py" "$@"

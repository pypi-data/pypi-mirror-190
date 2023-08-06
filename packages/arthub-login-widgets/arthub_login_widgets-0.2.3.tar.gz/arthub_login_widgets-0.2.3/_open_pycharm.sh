#!/bin/bash
#
# Run this to open PyCharm with the current directory including all
# dependencies from the package.py

_script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd ${_script_dir}

thm dev --ignore-standard-cmd tox -e ide

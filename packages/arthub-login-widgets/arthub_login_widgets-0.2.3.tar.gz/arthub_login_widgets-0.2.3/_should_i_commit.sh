#!/bin/bash
#
# Run this script to check this project against multiple code style checkers.
# E.g. PyLint, Flake8, etc.

# close_window means that the gitlab-ci is calling it and it needs to not
# keep an open pipe and exports docs to a different location.
if [ "$1" == "-close-window" ]; then close_window=y; fi

_script_dir=$( cd $( dirname ${BASH_SOURCE[0]} ) && pwd )
cd ${_script_dir}

thm dev --ignore-standard-cmd tox -e lint

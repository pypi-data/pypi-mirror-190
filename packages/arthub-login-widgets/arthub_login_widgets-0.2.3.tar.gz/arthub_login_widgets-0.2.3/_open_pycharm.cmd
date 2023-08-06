:: Run this to open PyCharm with the current directory including all
:: dependencies from the package.py

@echo off
cd %~dp0
thm dev --ignore-standard-cmd tox -e ide

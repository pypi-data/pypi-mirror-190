:: Run this script to check this project against multiple code style checkers.
:: E.g. PyLint, Flake8, etc.
@echo off
cd %~dp0

if [%1]==[-close_window] set close_window=y

if defined close_window (
    thm dev --ignore-standard-cmd tox -e lint
) else (
    cmd /k thm dev --ignore-standard-cmd tox -e lint
)

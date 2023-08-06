:: Run this to run all the tests in the directory.

@echo off
cd %~dp0

:: close_window means that the gitlab-ci is calling it and it needs to not keep an open pipe and exports docs to a different location.
if [%1]==[-close_window] set close_window=y

if defined close_window (
    thm dev --ignore-standard-cmd tox
) else (
    cmd /k thm dev --ignore-standard-cmd tox
)

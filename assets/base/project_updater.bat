@echo off

cd /d %~dp0

set "project_updater_exe=%CD%/project_updater.exe"

"%project_updater_exe%" update_project

exit /b 0
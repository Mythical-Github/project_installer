@echo off

cd /d %~dp0

set "project_directory=C:/Users/Mythical/Downloads/unreal_auto_mod"
set "content_zip_urls=https://github.com/Mythical-Github/unreal_auto_mod/releases/download/v1.6.1/unreal_auto_mod.zip"
set "project_updater_exe=%CD%/project_updater.exe"

set "command=update_project --project_directory "%project_directory%" --content_zip_urls "%content_zip_urls%""

"%project_updater_exe%" %command%

exit /b 0
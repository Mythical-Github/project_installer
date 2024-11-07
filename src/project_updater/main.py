import os
import sys
import shutil
import tomllib
import zipfile
import subprocess
from pathlib import Path

from project_updater import log_py as log


if getattr(sys, 'frozen', False):
    SCRIPT_DIR = Path(sys.executable).parent
else:
    SCRIPT_DIR = Path(__file__).resolve().parent


def run_app(exe_path: str, args: list = [], working_dir: str = None):
    command = [exe_path] + args
    log.log_message(f'Command: {" ".join(command)} is executing')
    if working_dir:
        if os.path.isdir(working_dir):
            os.chdir(working_dir)

    process = subprocess.Popen(command, cwd=working_dir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, shell=False)
    
    for line in iter(process.stdout.readline, ''):
        log.log_message(line.strip())

    process.stdout.close()
    process.wait()
    log.log_message(f'Command: {" ".join(command)} finished')


def update_project():
    pass

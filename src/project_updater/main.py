import os
import sys
import shutil
import tomllib
import zipfile
import subprocess
from pathlib import Path

import requests
from zipfile import ZipFile
import pyjson5 as json

from project_updater import log_py as log


if getattr(sys, 'frozen', False):
    SCRIPT_DIR = Path(sys.executable).parent
else:
    SCRIPT_DIR = Path(__file__).resolve().parent


JSON_PATH = f'{SCRIPT_DIR}/project_updater.json'


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


def get_recursive_backup_name(path):
    backup_path = f"{path}.bak"
    if os.path.exists(backup_path):
        return get_recursive_backup_name(backup_path)
    return backup_path

def create_recursive_backup(original_dir):
    if os.path.isdir(original_dir):
        backup_path = get_recursive_backup_name(original_dir)
        shutil.move(original_dir, backup_path)
        print(f"Moved '{original_dir}' to '{backup_path}'")


def load_settings(json_file_path):
    with open(json_file_path, 'r') as file:
        json_data = json.load(file)
    return json_data


def get_project_release_urls(json_file_path):
    settings = load_settings(json_file_path)
    return settings.get("Settings", {}).get("project_release_urls", [])


def get_exclude_names(json_file_path):
    settings = load_settings(json_file_path)
    return settings.get("Settings", {}).get("exclude_names", [])


def backup_files():
    backup_dir = os.path.join(SCRIPT_DIR, "backup")
    create_recursive_backup(backup_dir)
        
    os.makedirs(backup_dir, exist_ok=True)

    all_items = os.listdir(SCRIPT_DIR)
    
    exclude_names = get_exclude_names(JSON_PATH)

    items_to_backup = [
        item for item in all_items if item not in exclude_names
    ]

    for item in items_to_backup:
        item_path = os.path.join(SCRIPT_DIR, item)
        target_path = os.path.join(backup_dir, item)
        
        if os.path.isfile(item_path):
            shutil.move(item_path, target_path)
        elif os.path.isdir(item_path):
            if not item_path == backup_dir:
                shutil.move(item_path, target_path)

    print(f"Backup complete. {len(items_to_backup)} items moved to {backup_dir}")


def download_file(url, dest_folder=SCRIPT_DIR):
    local_filename = os.path.join(dest_folder, url.split('/')[-1])
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    print(f"Downloaded: {local_filename}")
    return local_filename


def unzip_release(zip_path, dest_folder=SCRIPT_DIR):
    with ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(dest_folder)
    os.remove(zip_path)
    print(f"Extracted and removed: {zip_path}")


def update_releases():
    for release_url in get_project_release_urls(JSON_PATH):
        zip_path = download_file(release_url)
        unzip_release(zip_path)


def cleanup_old_zips(directory=SCRIPT_DIR):
    for item in os.listdir(directory):
        if item.endswith('.zip'):
            os.remove(os.path.join(directory, item))
            print(f"Deleted old zip file: {item}")


def update_project():
    backup_files()
    update_releases()
    cleanup_old_zips()
import os
import sys
import shutil
import subprocess
from pathlib import Path
from zipfile import ZipFile

import requests
import pyjson5 as json

from project_updater.console import console


if getattr(sys, 'frozen', False):
    SCRIPT_DIR = Path(sys.executable).parent
else:
    SCRIPT_DIR = Path(__file__).resolve().parent


JSON_PATH = f'{SCRIPT_DIR}/project_updater.json'


def run_app(exe_path: str, args: list = [], working_dir: str = None):
    command = [exe_path] + args
    console.log(f'Command: {" ".join(command)} is executing')
    if working_dir:
        if os.path.isdir(working_dir):
            os.chdir(working_dir)
    subprocess.run(command, cwd=working_dir, text=True, shell=False)
    console.log(f'Command: {" ".join(command)} finished')


def get_recursive_backup_name(path):
    backup_path = f"{path}.bak"
    if os.path.exists(backup_path):
        return get_recursive_backup_name(backup_path)
    return backup_path


def create_recursive_backup(original_dir):
    if os.path.isdir(original_dir):
        backup_path = get_recursive_backup_name(original_dir)
        shutil.move(original_dir, backup_path)
        console.log(f"Moved '{original_dir}' to '{backup_path}'")


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

    console.log(f"Backup complete. {len(items_to_backup)} items moved to {backup_dir}")


def download_file(url, dest_folder=SCRIPT_DIR):
    local_filename = os.path.join(dest_folder, url.split('/')[-1])
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    console.log(f"Downloaded: {local_filename}")
    return local_filename


def unzip_release(zip_path, dest_folder=SCRIPT_DIR):
    with ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(dest_folder)
    os.remove(zip_path)
    console.log(f"Extracted and removed: {zip_path}")


def update_releases():
    for release_url in get_project_release_urls(JSON_PATH):
        zip_path = download_file(release_url)
        unzip_release(zip_path)


def cleanup_old_zips(directory=SCRIPT_DIR):
    for item in os.listdir(directory):
        if item.endswith('.zip'):
            os.remove(os.path.join(directory, item))
            console.log(f"Deleted old zip file: {item}")


def load_args_from_json(json_path):
    """
    Loads arguments from a JSON file.

    Args:
        json_path (str): Path to the JSON file containing argument key-value pairs.

    Returns:
        dict: Dictionary of arguments loaded from the JSON file.
    """
    try:
        with open(json_path, 'r') as json_file:
            args = json.load(json_file)
            console.log(f"Loaded arguments from {json_path}: {args}")
            return args
    except Exception as e:
        console.log(f"Error loading JSON file: {e}")
        return {}


def update_project(
    project_directory,
    content_urls,
    backup_directory_tree=True,
    backup_exclusions=None,
    delete_directory_tree=False,
    delete_exclusions=None,
    overwrite_files=True,
    overwrite_exclusions=None,
    dry_run=False,
    json_path=None
):
    
    if json_path:
        json_args = load_args_from_json(json_path)
        project_directory = json_args.get("project_directory", project_directory)
        content_urls = json_args.get("repo_release_urls", content_urls)
        backup_directory_tree = json_args.get("backup_directory_tree", backup_directory_tree)
        backup_exclusions = json_args.get("backup_exclusions", backup_exclusions)
        delete_directory_tree = json_args.get("delete_directory_tree", delete_directory_tree)
        delete_exclusions = json_args.get("delete_exclusions", delete_exclusions)
        overwrite_files = json_args.get("overwrite_files", overwrite_files)
        overwrite_exclusions = json_args.get("overwrite_exclusions", overwrite_exclusions)
        dry_run = json_args.get("dry_run", dry_run)

    """
    Updates a project by downloading and managing content as specified.

    Args:
        project_directory (str): Path of the directory of the project to update.
        repo_release_urls (str): A list of URLs of content to download and unzip to the specified project directory.
        backup_directory_tree (bool, optional): Whether to back up the project directory's content before installing new content.
        backup_exclusions (list, optional): List of file names and/or directories, relative to the project directory, to exclude from backup.
        delete_directory_tree (bool, optional): Whether to delete the project directory's content before installing new content.
        delete_exclusions (list, optional): List of file names and/or directories, relative to the project directory, to exclude from deletion.
        overwrite_files (bool, optional): Whether to overwrite existing files when installing new content.
        overwrite_exclusions (list, optional): List of file names and/or directories, relative to the project directory, to exclude from being overwritten.
        dry_run (bool, optional): If True, simulates the operations without performing any actions.
        json_path (str, optional): Path to a JSON file containing arguments to run the program with.

    Returns:
        None
    """
    console.log(f"Starting project update for directory: {project_directory}")

    if dry_run:
        console.log("Dry run enabled. No changes will be made.")
    
    if backup_directory_tree:
        console.log("Backing up the project directory...")
    
    if delete_directory_tree:
        console.log("Deleting contents of the project directory...")
    
    console.log(f"Downloading content from URLs: {content_urls}")

    console.log("Project update completed.")

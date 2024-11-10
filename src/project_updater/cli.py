from project_updater import main


OPTIONS = {
    "module": main,
    "commands": {
        "update_project": {
            "function_name": "update_project",
            "arg_help_pairs": [
                {"project_directory": {
                    "help": "path of the directory of the project to update",
                    "required": True
                }},
                {"content_urls": {
                    "help": "a list of URLs of content to download and unzip to the specified project directory",
                    "required": True
                }},
                {"backup_directory_tree": {
                    "help": "Whether or not the project directory's content should be backed up for installing new content, defaults to True",
                    "required": False
                }},
                {"backup_exclusions": {
                    "help": "list of file names and/or directory trees, relative to the specified project directory, to exclude from the backup",
                    "required": False
                }},
                {"delete_directory_tree": {
                    "help": "Whether or not the project directory's content should be deleted before installing new content, defaults to False",
                    "required": False
                }},
                {"delete_exclusions": {
                    "help": "list of file names and/or directory trees, relative to the specified project directory, to exclude from deletion",
                    "required": False
                }},
                {"overwrite_files": {
                    "help": "Whether or not to overwrite existing files when installing new content, defaults to True",
                    "required": False
                }},
                {"overwrite_exclusions": {
                    "help": "list of file names and/or directory trees, relative to the specified project directory, to exclude from being overwritten",
                    "required": False
                }},
                {"dry_run": {
                    "help": "Simulates the operations without performing any actions, useful for testing, defaults to False",
                    "required": False
                }},
                {"json_path": {
                    "help": "path to a JSON file that contains information about the arguments to run the program with",
                    "required": False
                }},
            ]
        }
    }
}

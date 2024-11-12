from project_updater import main


OPTIONS = {
    "module": main,
    "commands": {
        "update_project": {
            "function_name": "update_project",
            "arg_help_pairs": [
                {"project_directory": {
                    "help": "path of the directory of the project to update",
                    "required": True,
                    "use_nargs": False
                }},
                {"content_zip_urls": {
                    "help": "a list of URLs of zips to download and unzip to the specified project directory",
                    "required": True,
                    "use_nargs": True
                }},
                {"backup_directory_tree": {
                    "help": "Whether or not the project directory's content should be backed up for installing new content, defaults to True",
                    "required": False,
                    "use_nargs": False
                }},
                {"backup_exclusions": {
                    "help": "list of file names and/or directory trees, relative to the specified project directory, to exclude from the backup",
                    "required": False,
                    "use_nargs": True
                }},
                {"delete_directory_tree": {
                    "help": "Whether or not the project directory's content should be deleted before installing new content, defaults to False",
                    "required": False,
                    "use_nargs": False
                }},
                {"delete_exclusions": {
                    "help": "list of file names and/or directory trees, relative to the specified project directory, to exclude from deletion",
                    "required": False,
                    "use_nargs": True
                }},
                {"overwrite_files": {
                    "help": "Whether or not to overwrite existing files when installing new content, defaults to True",
                    "required": False,
                    "use_nargs": False
                }},
                {"overwrite_exclusions": {
                    "help": "list of file names and/or directory trees, relative to the specified project directory, to exclude from being overwritten",
                    "required": False,
                    "use_nargs": True
                }}
            ]
        }
    }
}

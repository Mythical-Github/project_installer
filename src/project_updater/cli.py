from project_updater import main

OPTIONS = {
    "module": main,
    "commands": {
        "update_project": {
            "function_name": "update_project",
            "arg_help_pairs": [
                {"repo_release_url": "url of the latest github repo release"}
            ]
        }
    }
}

import sys
from pathlib import Path

from project_updater import cli_py
from project_updater.console import console
from project_updater.cli_info import OPTIONS


if getattr(sys, 'frozen', False):
    SCRIPT_DIR = Path(sys.executable).parent
else:
    SCRIPT_DIR = Path(__file__).resolve().parent


def main():
    try:
        cli_py.cli_logic(OPTIONS)
    except Exception as error_message:
        console.log(str(error_message))


if __name__ == "__main__":
    main()

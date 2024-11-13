import os
import sys
from pathlib import Path

from project_updater import log_py
from project_updater import cli_py
from project_updater import log_info
from project_updater.cli_info import OPTIONS


if getattr(sys, 'frozen', False):
    SCRIPT_DIR = Path(sys.executable).parent
else:
    SCRIPT_DIR = Path(__file__).resolve().parent


def main():
    try:
        log_py.set_log_base_dir(os.path.join(SCRIPT_DIR, 'logs'))
        log_py.configure_logging(log_info.LOG_INFO)
        cli_py.cli_logic(OPTIONS)
    except Exception as error_message:
        log_py.log_message(str(error_message))


if __name__ == "__main__":
    main()

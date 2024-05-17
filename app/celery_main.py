#!/home/admin/venv_flask3/bin/python3

import logging
import os
from pathlib import Path
import sys
PATH_APP = Path(__file__).parent
if str(PATH_APP) not in sys.path:  # sys.platform == 'win32'
    sys.path.insert(0, str(PATH_APP))
os.chdir(PATH_APP)

import utils.arg_parse as arg_parse  # noqa: E402
arg_parse.init()
import my_logger  # noqa: F401, E402, I100

logger = logging.getLogger('debug_logger')
logger.debug(f'python:   {sys.executable}')
logger.debug(f'PATH_APP: {str(PATH_APP)}')

from app import app  # noqa: E402, I100, I202
import view  # noqa: F401, E402


if __name__ == '__main__':
    app.run(threaded=True)

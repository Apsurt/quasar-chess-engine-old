"""
This module initializes the logger for the application.
"""

#Built-in imports
import logging
import datetime
import os
import shutil

def clear_logs() -> None:
    """
    Clears the logs directory.
    """
    logs_path = 'logs'
    for filename in os.listdir(logs_path):
        file_path = os.path.join(logs_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except OSError as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

f_name = datetime.datetime.now().strftime('%Y-%m-%d_%H.%M.%S')
logger = logging.getLogger('chess')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(f'logs/{f_name}.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)
sh.setFormatter(formatter)
logger.addHandler(sh)

logger.info('Logger initialized.')

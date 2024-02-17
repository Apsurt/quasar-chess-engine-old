import logging
import datetime

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
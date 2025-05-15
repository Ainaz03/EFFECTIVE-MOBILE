import logging
import os

BASE_DIR = os.path.dirname(__file__)
LOG_PATH = os.path.join(BASE_DIR, 'parser.log')

def setup_logger():
    logger = logging.getLogger('my_logger')
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        fh = logging.FileHandler(LOG_PATH, encoding='utf-8')
        fh.setLevel(logging.INFO)
        fmt = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        fh.setFormatter(fmt)
        logger.addHandler(fh)
    return logger


logger = setup_logger()

import os

BASE_DIR = os.path.dirname(__file__)
DOWNLOAD_DIR = os.path.join(BASE_DIR, 'downloads')

BASE_URL = 'https://spimex.com/markets/oil_products/trades/results/'
BASE_BASE_URL = "https://spimex.com"
FILE_URL_REGEX = r'href="(/upload/reports/oil_xls/oil_xls_(\d{14})\.xls.*?)"'
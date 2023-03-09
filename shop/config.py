from . import utils
# import utils
import os
import sys
from dotenv import load_dotenv, find_dotenv
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

load_dotenv(find_dotenv())


MARKET = 'Shop'



URL = 'https://shop.kz'

HEADERS = {
    'authority': 'shop.kz',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/108.0.0.0 Safari/537.36 OPR/94.0.0.0',
}

COOKIES = {
    'iRegionSectionId': '3',
    'iRegionSectionName': '%D0%90%D1%81%D1%82%D0%B0%D0%BD%D0%B0',    #   Астана
}

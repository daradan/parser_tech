import os
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())


MARKET = 'Technodom'

URL_C = 'https://api.technodom.kz/menu/api/v1/menu/katalog'
URL_P = 'https://api.technodom.kz/katalog/api/v1/products/category/'

CITY_ID = '5f5f1e3b6a600b98a31fddb6'  # Astana
LIMIT = 200

HEADERS = {
    'Host': 'api.technodom.kz',
    'content-language': 'ru-RU',
    'content-language-system': 'ru',
    'user-agent': os.getenv('TECHNODOM_USER_AGENT'),
}

PARAMS = {
    'city_id': CITY_ID,
}

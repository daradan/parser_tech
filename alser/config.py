import requests
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


MARKET = 'Alser'
URL = 'https://mobapi.alser.kz/v2'
URL_P = 'https://alser.kz/p'

LIMIT = 50

HEADERS = {
    'Content-Type': 'application/json; charset=UTF-8',
    'Host': 'mobapi.alser.kz',
    'User-Agent': os.getenv('ALSER_USER_AGENT'),
}

JSON_DATA = {
    'category_id': 4,
    'filters': {},
    'limit': LIMIT,
    'page': 1,
    'prices': {},
    'sort': 'newest',
    'with_specs': True,
}


if __name__ == '__main__':
    response = requests.post(f'{URL}/products', headers=HEADERS, json=JSON_DATA)
    print(response.text)

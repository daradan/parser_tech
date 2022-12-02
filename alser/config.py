import requests


MARKET = 'Alser'
URL = 'https://mobapi.alser.kz/v2'
URL_P = 'https://alser.kz/p'

HEADERS = {
    'Content-Type': 'application/json; charset=UTF-8',
    'Host': 'mobapi.alser.kz',
    'User-Agent': 'okhttp/4.9.3',
}

JSON_DATA = {
    'category_id': 4,
    'filters': {},
    'limit': 50,
    'page': 1,
    'prices': {},
    'sort': 'newest',
    'with_specs': True,
}


if __name__ == '__main__':
    response = requests.post(f'{URL}/products', headers=HEADERS, json=JSON_DATA)
    print(response.text)

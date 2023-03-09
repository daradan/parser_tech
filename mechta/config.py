import os
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())

MARKET = 'Mechta'

URL_C = 'https://www.mechta.kz/api/v1/header/catalog-hierarchy'
URL_P = 'https://www.mechta.kz/api/new/catalog'
URL_PR = 'https://www.mechta.kz/api/v1/mindbox/actions/catalog'

LIMIT = 200

HEADERS = {
    'Host': 'www.mechta.kz',
    'x-mechta-app': os.getenv('MECHTA_APP'),
    'x-city-code': 's1',    # Astana
    'user-agent': os.getenv('MECHTA_USER_AGENT'),
}

PARAMS = {
    'section': 'noutbuki',
    'properties': '',
    'order': 'sort',
    'adesc': 'desc',
    'page': '1',
    'page_limit': LIMIT,
    'catalog': 'true',
}

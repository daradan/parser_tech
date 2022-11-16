from . import utils
import os
import sys
from dotenv import load_dotenv, find_dotenv
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

load_dotenv(find_dotenv())


MARKET = 'Sulpak'

URL = 'https://api.sulpak.kz/v0/kz/3/3'
URL_IMAGE = 'https://object.pscloud.io/cms/cms/Photo/'
URL_BEARER = 'https://api.sulpak.kz/authentication/token'

HEADER_BEARER = {
    'Accept-Charset': 'UTF-8',
    'Content-Type': 'application/json; charset=UTF-8',
    'password': os.getenv('SULPAK_PASSWORD'),
    'login': os.getenv('SULPAK_USER'),
    'NetworkConsumer': 'mobile-app',
    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 12; 21081111RG Build/SP1A.210812.016)',
    'Host': 'api.sulpak.kz',
}

HEADER = {
    'Accept-Charset': 'UTF-8',
    'Authorization': f"Bearer {utils.get_bearer_token()}",
    'NetworkConsumer': 'mobile-app',
    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 12; 21081111RG Build/SP1A.210812.016)',
    'Host': 'api.sulpak.kz',
}

JSON_DATA = {
    'page': 1,
    'classId': 83,
    'goodsPerPage': 8,
    'orderBy': 5,
    'priceFrom': 0,
    'priceTo': 2147483647,
    'catalogObjectFilter': {
        'itemsCount': 0,
        'minPrice': 0,
        'maxPrice': 0,
        'tagsIds': None,
        'availability': None,
        'signs': None,
        'rating': None,
        'filtersAvailabilitiesAndSignsCounts': None,
        'stocks': None,
        'tags': None,
        'properties': None,
        'selectedProperties': None,
        'ratings': None,
        'handAddedLinks': None,
    },
    'commentsCount': None,
    'query': None,
}

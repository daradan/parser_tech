from . import utils
# import utils
import os
import sys
from dotenv import load_dotenv, find_dotenv

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

load_dotenv(find_dotenv())

MARKET = 'DNS'

URL = 'https://www.dns-shop.kz'
URL_C = 'https://restapi.dns-shop.kz/v1/get-menu'
URL_P = 'https://www.dns-shop.kz/ajax-state/product-buy/'

HEADERS = {
    'Host': 'www.dns-shop.kz',
    'Sec-Ch-Ua': '"Chromium";v="109", "Not_A Brand";v="99"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Linux"',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': os.getenv('DNS_USER_AGENT'),
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'close',
}

HEADERS_C = {
    'Host': 'restapi.dns-shop.kz',
    'Accept': 'application/json, text/plain, */*',
    'Siteid': '8c2e120b-8732-48a7-8178-0e04d47962d8',
    'Cityid': '7c1a64af-5a32-11eb-a227-00155dd9e604',
    'User-Agent': os.getenv('DNS_USER_AGENT'),
    'Referer': 'https://www.dns-shop.kz/',
    'Accept-Language': 'en-US,en;q=0.9',
}

HEADERS_P = {
    'Host': 'www.dns-shop.kz',
    # 'Content-Length': '1338',
    'Cache-Control': 'max-age=0',
    'Sec-Ch-Ua': '"Not A(Brand";v="24", "Chromium";v="110"',
    'Content-Type': 'application/x-www-form-urlencoded',
    'X-Csrf-Token': 'YZR3AAJXjaUnDIZ8pRh3n0HPPt7wZIIgxiubeFg1VHBUwUdZRD36nGNkwS3TRxXpK6wPqsRUwRWlHes7KEABFA==',
    'X-Requested-With': 'XMLHttpRequest',
    'Sec-Ch-Ua-Mobile': '?0',
    'User-Agent': os.getenv('DNS_USER_AGENT'),
    'Sec-Ch-Ua-Platform': '"Linux"',
    'Accept': '*/*',
    'Origin': 'https://www.dns-shop.kz',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://www.dns-shop.kz/catalog/17a899cd16404e77/processory/no-referrer',
    # 'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9',
    # 'Cookie': '__ddg1_=WWCZQr32G3fFw3sOhSmS; current_path=450b3c4f8da2c63f7a2f14910a100cdc46aa5070bfc26be651c5598a13457d54a%3A2%3A%7Bi%3A0%3Bs%3A12%3A%22current_path%22%3Bi%3A1%3Bs%3A114%3A%22%7B%22city%22%3A%227c1a64af-5a32-11eb-a227-00155dd9e604%22%2C%22cityName%22%3A%22%5Cu0410%5Cu0441%5Cu0442%5Cu0430%5Cu043d%5Cu0430%22%2C%22method%22%3A%22geoip%22%7D%22%3B%7D; phonesIdent=d7b75ecb4dac1b8e6299875d3f8baa4ccadf50bf8436562d56bdf4ef6dd8e132a%3A2%3A%7Bi%3A0%3Bs%3A11%3A%22phonesIdent%22%3Bi%3A1%3Bs%3A36%3A%221f1ea8ee-e0cf-4706-8698-64f62916a9a1%22%3B%7D; cartUserCookieIdent_v3=2a64e53c981e5a14b946cbaa8cadfc47bdf8463f202cabf947ca4a026697338ea%3A2%3A%7Bi%3A0%3Bs%3A22%3A%22cartUserCookieIdent_v3%22%3Bi%3A1%3Bs%3A36%3A%22f93f74d1-1260-3a60-938a-886d885d3547%22%3B%7D; _gcl_au=1.1.485012077.1675014668; _ym_uid=1675014669546322685; _ym_d=1675014669; _fbp=fb.1.1675014669777.771050600; _ab_=%7B%22mobile-filters-position%22%3A%22current_position%22%7D; PHPSESSID=2464a4c04c6697d777a130a4848eac2a; _ym_isad=2; _gid=GA1.2.853622303.1677072721; _ga=GA1.2.358062627.1675014669; _ga_HT4YQ5ZZKL=GS1.1.1677078699.7.0.1677078702.0.0.0; lang=ru; _csrf=f5a2636af1101627c00b21a518d9ec8b8f9cc14ff7f7592ae160481c561a8caaa%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%225U0YFjw9DhGQv_bvjc1t40C5c6pCpuUd%22%3B%7D',
}

PARAMS_C = {
    'maxMenuLevel': '3',
}

PARAMS_P = {
    'cityId': '2363',  # astana
    'langId': 'ru',
    'v': '2',
}

CITY_PATH = '450b3c4f8da2c63f7a2f14910a100cdc46aa5070bfc26be651c5598a13457d54a%3A2%3A%7Bi%3A0%3Bs%3A12%3A%22' \
            'current_path%22%3Bi%3A1%3Bs%3A114%3A%22%7B%22city%22%3A%227c1a64af-5a32-11eb-a227-00155dd9e604%22%2C%22' \
            'cityName%22%3A%22%5Cu0410%5Cu0441%5Cu0442%5Cu0430%5Cu043d%5Cu0430%22%2C%22method%22%3A%22geoip%22%7D%22%3B%7D'
DOMAIN = '.dns-shop.kz'
COOKIE = {'name': 'current_path', 'value': CITY_PATH, 'domain': DOMAIN, 'path': '/'}

# LANG = 'ru'
# CITY = 'astana'
# CITY_PATH = 'f9a36f5471f403da91cad096f4bd7f794d701cd89c8e0ff446557353ad1b6ec4a%3A2%3A%7Bi%3A0%3Bs%3A12%3A%22' \
#             'current_path%22%3Bi%3A1%3Bs%3A115%3A%22%7B%22' \
#             'city%22%3A%227c1a64af-5a32-11eb-a227-00155dd9e604%22%2C%22' \
#             'cityName%22%3A%22%5Cu0410%5Cu0441%5Cu0442%5Cu0430%5Cu043d%5Cu0430%22%2C%22' \
#             'method%22%3A%22manual%22%7D%22%3B%7D'
#
# HEADERS = {
#     'Host': 'restapi.dns-shop.kz',
#     'Accept': 'application/json, text/plain, */*',
#     'Siteid': '8c2e120b-8732-48a7-8178-0e04d47962d8',
#     'Cityid': '7c1a64af-5a32-11eb-a227-00155dd9e604',
#     'User-Agent': os.getenv('DNS_USER_AGENT'),
#     'Referer': 'https://www.dns-shop.kz/',
#     'Accept-Language': 'en-US,en;q=0.9',
# }
#
# PARAMS = {
#     'maxMenuLevel': '3',
# }
#
# COOKIES = [
#     {'name':'lang', 'value':LANG, 'path':'/', 'domain':DOMAIN},
#     {'name':'city_path', 'value':CITY, 'path':'/', 'domain':DOMAIN},
#     {'name': 'current_path', 'value':CITY_PATH, 'path': '/', 'domain':DOMAIN}
# ]

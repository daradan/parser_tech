import json
import requests
from bs4 import BeautifulSoup

from . import config
# import config
import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from proxies import Proxies


def get_categories(session: requests.Session, proxies: list[str]) -> list:
    if not proxies:
        os.remove('../../proxies.json')
        session.cookies.clear()
        proxies = Proxies().start()
        return get_categories(session, proxies)
    categories = []
    try:
        response = session.get(config.URL, headers=config.HEADERS,
                               proxies={'https': proxies[0]}, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        categories_raw = soup.find_all('li', class_='bx-nav-3-lvl')
        for category_raw in categories_raw:
            if category_raw.a:
                categories.append(category_raw.a.get('href'))
        return categories
    except requests.exceptions.ConnectionError as e:
        proxies.pop(0)
        session.cookies.clear()
        return get_categories(session, proxies)
# def get_categories(session) -> list:
#     return ['/planshety/']

# categories = []
#
#
# def get_subcategory(category_obj):
#     for subcategory in category_obj:
#         if subcategory['children']:
#             get_subcategory(subcategory['children'])
#         else:
#             temp_dict = {
#                 # 'id': subcategory.get('id'),
#                 # 'code_1c': subcategory.get('code_1c'),
#                 'name': subcategory['title'],
#                 'id': subcategory['id'],
#                 'url': subcategory['uniqueName']
#             }
#             categories.append(temp_dict)
#
#
# def get_categories(session) -> list:
#     # session = requests.session()
#     response = session.get(f"{config.URL}/menu/catalog/2/false", headers=config.HEADER)
#     json_loads = json.loads(response.text)
#     for subcategories in json_loads:
#         get_subcategory(subcategories['children'])
#     return categories


if __name__ == '__main__':
    print(get_categories(requests.session(), Proxies().start()))

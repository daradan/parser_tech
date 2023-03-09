import requests
import json

from . import config
# import config
import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from proxies import Proxies

categories = []


def get_subcategory(category_obj: dict):
    for subcategory in category_obj.values():
        if subcategory.get('menu'):
            get_subcategory(subcategory['menu'])
        else:
            temp_dict = {
                'name': subcategory.get('name'),
                'url': subcategory.get('code')
            }
            categories.append(temp_dict)


def get_categories(session: requests.Session, proxies: list[str]) -> list:
    if not proxies:
        os.remove('../../proxies.json')
        session.cookies.clear()
        proxies = Proxies().start()
        return get_categories(session, proxies)
    try:
        response = session.get(f"{config.URL_C}", headers=config.HEADERS, proxies={'https': proxies[0]}, timeout=10)
        if response.status_code != 200:
            logging.info(f"Status code not 200 in proxy {proxies[0]}. Try to use next proxy")
            proxies.pop(0)
            session.cookies.clear()
            return get_categories(session, proxies)
        json_loads = json.loads(response.text)
        for subcategories in json_loads['data']['catalog'].values():
            get_subcategory(subcategories['menu'])
        return categories
    except requests.exceptions.ConnectionError as e:
        proxies.pop(0)
        session.cookies.clear()
        return get_categories(session, proxies)


if __name__ == '__main__':
    session = requests.session()
    print(get_categories(session, Proxies().start()))

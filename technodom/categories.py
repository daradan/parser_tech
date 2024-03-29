from typing import List
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


def get_subcategory(category_obj):
    for subcategory in category_obj:
        if subcategory.get('children'):
            get_subcategory(subcategory['children'])
        else:
            temp_dict = {
                'name': subcategory.get('title'),
                'url': subcategory.get('uri')
            }
            categories.append(temp_dict)


def get_categories(session: requests.Session, proxies: list[str]) -> List[dict]:
    if not proxies:
        os.remove('../../proxies.json')
        session.cookies.clear()
        proxies = Proxies().start()
        return get_categories(session, proxies)
    try:
        response = session.get(f"{config.URL_C}", headers=config.HEADERS, params=config.PARAMS,
                               proxies={'https': proxies[0]}, timeout=10)
        if response.status_code != 200:
            proxies.pop(0)
            session.cookies.clear()
            return get_categories(session, proxies)
        json_loads = json.loads(response.text)
        for subcategories in json_loads.get('items'):
            get_subcategory(subcategories['children'])
        return categories
    except requests.exceptions.ConnectionError as e:
        proxies.pop(0)
        session.cookies.clear()
        return get_categories(session, proxies)


if __name__ == '__main__':
    print(get_categories(requests.session(), Proxies().start()))

from typing import List
import requests
import json
import os
import sys

from . import config
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from proxies import Proxies


categories = []


def get_subcategory(category_obj):
    for subcategory in category_obj:
        if subcategory.get('childs'):
            get_subcategory(subcategory['childs'])
        else:
            temp_dict = {
                'id': subcategory.get('id'),
                'name': subcategory.get('title'),
                'url': config.URL + subcategory.get('url')
            }
            categories.append(temp_dict)


def get_categories(session: requests.Session, proxies: list[str]) -> List[dict]:
    if not proxies:
        os.remove('../../proxies.json')
        session.cookies.clear()
        proxies = Proxies().start()
        return get_categories(session, proxies)
    try:
        response = session.get(f"{config.URL_C}", headers=config.HEADERS_C, params=config.PARAMS_C,
                               proxies={'https': proxies[0]}, timeout=10)
        if response.status_code != 200:
            proxies.pop(0)
            session.cookies.clear()
            return get_categories(session, proxies)
    except requests.exceptions.ConnectionError:
        proxies.pop(0)
        session.cookies.clear()
        return get_categories(session, proxies)
    json_loads = json.loads(response.text)
    for subcategories in json_loads.get('data'):
        if subcategories.get('childs'):
            get_subcategory(subcategories['childs'])
    return categories


if __name__ == '__main__':
    print(get_categories(requests.session(), ['xx.xx.xx.xx:xx']))

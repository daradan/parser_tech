import requests
import json

from . import config
# import config


categories = []


def get_subcategory(category_obj):
    for subcategory in category_obj:
        if subcategory['children']:
            get_subcategory(subcategory['children'])
        else:
            temp_dict = {
                # 'id': subcategory.get('id'),
                # 'code_1c': subcategory.get('code_1c'),
                'name': subcategory['title'],
                'id': subcategory['id'],
                'url': subcategory['uniqueName']
            }
            categories.append(temp_dict)


def get_categories(session: requests.Session, proxies: list[str]) -> list:
    try:
        response = session.get(f"{config.URL}/categories", headers=config.HEADERS, proxies={'https': proxies[0]}, verify=False, timeout=10)
    except requests.exceptions.ConnectionError:
        proxies.pop()
        session.cookies.clear()
        return get_categories(session, proxies)
    if response.status_code != 200:
        proxies.pop()
        session.cookies.clear()
        return get_categories(session, proxies)
    json_loads = json.loads(response.text)
    for subcategories in json_loads.get('data'):
        get_subcategory(subcategories['children'])
    return categories


if __name__ == '__main__':
    print(get_categories(requests.session(), ['xx.xx.xx.173:3128']))

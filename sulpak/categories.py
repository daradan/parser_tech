import json
import requests
from . import config
# import config


categories_ids = {}


def get_subcategory(category_obj):
    for subcategory in category_obj:
        if subcategory['children']:
            get_subcategory(subcategory['children'])
        else:
            category_id = subcategory['id']
            category_name = subcategory['title']
            categories_ids[category_id] = category_name


def get_categories(session):
    # session = requests.session()
    response = session.get(f"{config.URL}/menu/catalog/2/false", headers=config.HEADER)
    json_loads = json.loads(response.text)
    for subcategories in json_loads:
        get_subcategory(subcategories['children'])
    return categories_ids


if __name__ == '__main__':
    print(get_categories(requests.session()))

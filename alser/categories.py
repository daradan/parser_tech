import requests
import json
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


def get_categories() -> dict:
    response = requests.get(f"{config.URL}/categories", headers=config.HEADERS)
    json_loads = json.loads(response.text)
    for subcategories in json_loads.get('data'):
        get_subcategory(subcategories['children'])
    return categories_ids


if __name__ == '__main__':
    print(get_categories())

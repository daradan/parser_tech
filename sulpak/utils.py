from . import config
# import config
from .schemas import ProductSchema, PriceSchema
from .models import SulpakProducts, SulpakPrices

import requests
import sys
import os
from typing import List
from dotenv import load_dotenv, find_dotenv
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import global_config
import global_utils

load_dotenv(find_dotenv())


def get_bearer_token() -> str:
    response = requests.post('https://api.sulpak.kz/authentication/token', headers=config.HEADER_BEARER, json={})
    return response.text


def make_image_url(images: list) -> str:
    for index, image in enumerate(images):
        images[index] = f"{config.URL_IMAGE}{image}"
    return ','.join(images)


def make_characteristics(characteristics: list) -> str:
    try:
        for index, item in enumerate(characteristics):
            characteristics[index] = f"{item['title']}: {item['value']['value']}"
        return '\n'.join(characteristics)
    except:
        return ''


def make_image_caption(product_obj: ProductSchema, all_prices: List[SulpakPrices]) -> str:
    fixed_category = global_utils.fix_category(product_obj.category)
    fixed_brand = global_utils.fix_category(product_obj.brand)
    image_caption = f"<b>{product_obj.name}</b>\n" \
                    f"#{config.MARKET} #{fixed_category} #{fixed_brand}\n\n" \
                    f"{fix_characteristics(product_obj.characteristics)}\n\n" \
                    f"{global_utils.fix_all_prices(all_prices)}\n" \
                    f"<a href='{product_obj.url}{global_utils.make_utm_tags()}'>Купить</a>\n\n" \
                    f"{global_config.TG_CHANNEL}"
    return image_caption


def fix_characteristics(characteristics: str) -> str:
    need_to_replace = ['<p>', '</p>']
    for change in need_to_replace:
        characteristics = characteristics.replace(change, '')
    return characteristics

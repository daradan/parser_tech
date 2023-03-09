from . import config
# import config
from .schemas import ProductSchema, PriceSchema
from .models import ShopProducts, ShopPrices

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


def make_cat_urls(categories: list) -> list:
    data = []
    for category in categories:
        data.append(f"{config.URL}{category}") #filter/astana-is-v_nalichii-or-ojidaem-or-dostavim/apply/")
    return data


def make_image_caption(product_obj: ProductSchema, all_prices: List[ShopPrices]) -> str:
    fixed_category = global_utils.fix_category(product_obj.category)
    fixed_brand = global_utils.fix_category(product_obj.brand)
    image_caption = f"<b>{product_obj.name}</b>\n" \
                    f"#{config.MARKET} #{fixed_category} #{fixed_brand}\n\n" \
                    f"{global_utils.fix_all_prices(all_prices)}\n" \
                    f"<a href='{product_obj.url}{global_utils.make_utm_tags()}'>Купить</a>\n\n" \
                    f"{global_config.TG_CHANNEL}"
    if product_obj.characteristics:
        image_caption = image_caption.replace('\n\n', f"\n\n{product_obj.characteristics}\n\n", 1)
    return image_caption

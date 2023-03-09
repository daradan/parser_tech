from . import config
from .schemas import ProductSchema, PriceSchema
from .models import MechtaProducts, MechtaPrices
from typing import List
import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import global_config
import global_utils


def get_product_ids(products_items: list) -> str:
    product_ids = []
    for product in products_items:
        product_ids.append(str(product['id']))
    return ','.join(product_ids)


def merge_price_to_products(products: dict, prices: dict) -> dict:
    for key, value in prices.items():
        for num, prdct_value in enumerate(products['items']):
            if value['id'] == prdct_value['id']:
                products['items'][num].update(value)
    return products


def make_image_caption(product_obj: ProductSchema, all_prices: List[MechtaPrices]) -> str:
    fixed_category = global_utils.fix_category(product_obj.category)
    fixed_brand = global_utils.fix_category(product_obj.brand)
    image_caption = f"<b>{product_obj.name}</b>\n" \
                    f"#{config.MARKET} #{fixed_category} #{fixed_brand}\n\n" \
                    f"{global_utils.fix_all_prices(all_prices)}\n" \
                    f"<a href='{product_obj.url}/{global_utils.make_utm_tags()}'>Купить</a>\n\n" \
                    f"{global_config.TG_CHANNEL}"
    return image_caption

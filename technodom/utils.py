from . import config
from .schemas import ProductSchema, PriceSchema
from .models import TechnodomProducts, TechnodomPrices

import sys
import os
from typing import List
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import global_config
import global_utils


def make_url(category: dict) -> str:
    url_raw = category['url'].split('/')[-1]
    url = f"{config.URL_P}{url_raw}"
    return url


def make_images(images: list) -> str:
    img_lst = []
    for image in images:
        img_lst.append(f"https://api.technodom.kz/f3/api/v1/images/1080/1080/{image}.jpg")
    return ','.join(img_lst)


def make_image_caption(product_obj: ProductSchema, all_prices: List[TechnodomPrices]) -> str:
    fixed_category = global_utils.fix_category(product_obj.category)
    fixed_brand = global_utils.fix_category(product_obj.brand)
    image_caption = f"<b>{product_obj.name}</b>\n" \
                    f"<b>{product_obj.color}</b>\n" \
                    f"#{config.MARKET} #{fixed_category} #{fixed_brand}\n\n" \
                    f"{global_utils.fix_all_prices(all_prices)}\n" \
                    f"<a href='{product_obj.url}{global_utils.make_utm_tags()}'>Купить</a>\n\n" \
                    f"{global_config.TG_CHANNEL}"
    return image_caption

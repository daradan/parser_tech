from . import config
# import config
from .schemas import ProductSchema, PriceSchema
from .models import DnsProducts, DnsPrices

import requests
from bs4 import BeautifulSoup
import sys
import os
import random
from typing import List
from dotenv import load_dotenv, find_dotenv
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import global_config
import global_utils

load_dotenv(find_dotenv())


# def get_prices(session: requests.Session, items: list) -> dict:
#     ids = []
#     fake_ids =
#     product_ids_prices = {}
#     for item in items:
#         soup = BeautifulSoup(item, 'html.parser')




def make_image_caption(product_obj: ProductSchema, all_prices: List[DnsPrices]) -> str:
    fixed_category = global_utils.fix_category(product_obj.category)
    image_caption = f"<b>{product_obj.name}</b>\n" \
                    f"#{config.MARKET} #{fixed_category}\n\n" \
                    f"{global_utils.fix_all_prices(all_prices)}\n" \
                    f"<a href='{product_obj.url}{global_utils.make_utm_tags()}'>Купить</a>\n\n" \
                    f"{global_config.TG_CHANNEL}"
    if product_obj.characteristics:
        image_caption = image_caption.replace('\n\n', f"\n\n{product_obj.characteristics}\n\n", 1)
    return image_caption

from __future__ import annotations

import requests
import json
import logging
from random import randrange, shuffle
from time import sleep
from typing import List

from technodom import categories, config, utils
from .schemas import ProductSchema, PriceSchema
from .models import TechnodomPrices
from .crud import TechnodomProductsCrud, TechnodomPricesCrud

import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from database import SessionLocal
import send_to_tg
import global_utils
import global_config
from proxies import Proxies


class TechnodomParser:
    def __init__(self):
        self.session = requests.Session()
        self.db_session = SessionLocal()
        self.products_crud: TechnodomProductsCrud = TechnodomProductsCrud(session=self.db_session)
        self.prices_crud: TechnodomPricesCrud = TechnodomPricesCrud(session=self.db_session)
        self.proxies = Proxies().start()

    def start(self):
        logging.info(f"{config.MARKET} Parser START")
        all_categories = categories.get_categories(self.session, self.proxies)
        shuffle(all_categories)
        for category in all_categories:
            url = utils.make_url(category)
            page = 1
            try:
                response = self.get_response(category, url, page)
            except:
                continue
            if not response:
                continue
            response = json.loads(response.text)
            total_product = response['total'] - config.LIMIT
            products = response['payload']
            while total_product > 0:
                page += 1
                try:
                    append = self.get_response(category, url, page)
                except:
                    continue
                if not append:
                    continue
                append = json.loads(append.text)
                products.extend(append['payload'])
                total_product -= config.LIMIT
            self.parse_products(products, category['name'])
            sleep(randrange(global_config.SLEEP_START, global_config.SLEEP_FINISH))
        logging.info(f"{config.MARKET} Parser END")

    def get_response(self, category: dict, url: str, page: int) -> requests.models.Response | None:
        if not self.proxies:
            os.remove('../../proxies.json')
            self.session.cookies.clear()
            self.proxies = Proxies().start()
            return self.get_response(category, page)
        params = config.PARAMS
        params['page'] = page
        params['limit'] = config.LIMIT
        try:
            response = self.session.get(url, headers=config.HEADERS, params=config.PARAMS,
                                        proxies={'https': self.proxies[0]}, timeout=10)
            if response.status_code != 200:
                logging.info(f"Status code not 200 in proxy {self.proxies[0]}. Try to use next proxy")
                self.proxies.pop(0)
                self.session.cookies.clear()
                return self.get_response(category, url, page)
            return response
        except requests.exceptions.ConnectionError as e:
            logging.info(f"Proxy {self.proxies[0]} doesn't work. Try to use next proxy")
            self.proxies.pop(0)
            self.session.cookies.clear()
            return self.get_response(category, url, page)

    def parse_products(self, products: list, category: str) -> None:
        for product in products:
            if not product.get('title') \
                    or not product.get('uri') \
                    or not product.get('sku') \
                    or not product.get('categories_ru') \
                    or not product.get('images'):
                logging.exception(f"{config.MARKET}, can't find some keys. {product}")
                continue
            product_obj = {
                'name': product['title'],
                'url': f"https://www.technodom.kz/p/{product['uri']}",
                'sku': product['sku'],
                'brand': product.get('brand', None),
                'category': ','.join(product['categories_ru']),
                'color': product['color'].get('title', None),
                'images': utils.make_images(product['images'])
            }
            product_obj = ProductSchema(**product_obj)
            price_obj = PriceSchema(price=int(product['price']))
            self.check_data_from_db(product_obj, price_obj, category)

    def check_data_from_db(self, product_obj: ProductSchema, price_obj: PriceSchema, category: str) -> None:
        product = self.products_crud.get_or_create(product_obj)
        price_obj.product_id = product.id
        last_price = self.prices_crud.get_last_price(product.id)
        if last_price:
            discount = global_utils.get_percentage(price_obj.price, int(last_price.price))
            price_obj.discount = discount
        if not last_price or price_obj.discount != '0':
            self.prices_crud.insert(price_obj)
            if not last_price:
                return
            last_n_prices: List[TechnodomPrices] = self.prices_crud.get_last_n_prices(product.id)
            is_lowest_price = global_utils.check_lowest_price(price_obj.price, last_n_prices[1:], config.MARKET)
            is_in_stop_products_list = global_utils.is_in_stop_prdcts_list(product_obj.name)
            is_in_stop_categories_list = global_utils.is_in_stop_ctgrs_list(category)
            if is_lowest_price and not is_in_stop_products_list and not is_in_stop_categories_list:
                last_n_prices_cleared = global_utils.clear_all_prices(last_n_prices)
                image_caption = utils.make_image_caption(product_obj, last_n_prices_cleared)
                try:
                    send_tg = send_to_tg.send_as_photo(
                        image_caption, product_obj.images.split(',')[0], global_config.TG_CHANNEL
                    )
                    if global_utils.is_in_pc_ctgrs_list(category):
                        send_tg = send_to_tg.send_as_photo(
                            image_caption, product_obj.images.split(',')[0], global_config.TG_CHANNEL_PC
                        )
                    logging.info(f"TG status_code - {send_tg}. Product id - {product.id}")
                except:
                    return


if __name__ == '__main__':
    logging.basicConfig(
        handlers=[logging.FileHandler('technodom_parser.log', 'a+', 'utf-8')],
        format="%(asctime)s %(levelname)s:%(message)s",
        level=logging.INFO,
    )
    TechnodomParser().start()

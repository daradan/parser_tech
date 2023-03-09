import requests
import json
import logging
from random import randrange, shuffle
from typing import List
from time import sleep

from mechta import categories, config, utils
from .schemas import ProductSchema, PriceSchema
from .crud import MechtaProductsCrud, MechtaPricesCrud
from .models import MechtaPrices

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


class MechtaParser:
    def __init__(self):
        self.session = requests.Session()
        self.db_session = SessionLocal()
        self.products_crud: MechtaProductsCrud = MechtaProductsCrud(session=self.db_session)
        self.prices_crud: MechtaPricesCrud = MechtaPricesCrud(session=self.db_session)
        self.proxies = Proxies().start()

    def start(self):
        logging.info(f"{config.MARKET} Parser START")
        all_categories = categories.get_categories(self.session, self.proxies)
        shuffle(all_categories)
        for category in all_categories:
            page = 1
            try:
                response = self.get_response(config.URL_P, category, page)
            except:
                continue
            if not response:
                continue
            total_product = response['all_items_count'] - config.LIMIT
            products = response['items']
            while total_product > 0:
                page += 1
                try:
                    append = self.get_response(config.URL_P, category, page)
                except:
                    continue
                if not append:
                    continue
                products.extend(append['items'])
                total_product -= config.LIMIT
            self.parse_products(products)
            sleep(randrange(global_config.SLEEP_START, global_config.SLEEP_FINISH))
        logging.info(f"{config.MARKET} Parser END")

    def get_response(self, url: str, category: dict, page: int) -> dict | None:
        if not self.proxies:
            os.remove('../../proxies.json')
            self.session.cookies.clear()
            self.proxies = Proxies().start()
            return self.get_response(url, category, page)
        params = config.PARAMS
        params['page'] = page
        params['section'] = category['url']
        try:
            products = self.session.get(url, headers=config.HEADERS, params=config.PARAMS,
                                        proxies={'https': self.proxies[0]}, timeout=10)
            if products.status_code != 200:
                logging.info(f"Status code not 200 in proxy {self.proxies[0]}. Try to use next proxy")
                self.proxies.pop(0)
                self.session.cookies.clear()
                return self.get_response(url, category, page)
            products_json = json.loads(products.text)
            product_ids = utils.get_product_ids(products_json['data']['items'])
            if not product_ids:
                return None
        except requests.exceptions.ConnectionError as e:
            logging.info(f"Proxy {self.proxies[0]} doesn't work. Try to use next proxy")
            self.proxies.pop(0)
            self.session.cookies.clear()
            return self.get_response(url, category, page)

        data = {'product_ids': product_ids}
        try:
            prices = self.session.post(config.URL_PR, headers=config.HEADERS, data=data,
                                       proxies={'https': self.proxies[0]}, timeout=10)
            if products.status_code != 200:
                logging.info(f"Status code not 200 in proxy {self.proxies[0]}. Try to use next proxy")
                self.proxies.pop(0)
                self.session.cookies.clear()
                return self.get_response(url, category, page)
            prices_json = json.loads(prices.text)

            if not products_json['data']['items'] or not prices_json['data']:
                return None

            merged_products = utils.merge_price_to_products(products_json['data'], prices_json['data'])
            return merged_products
        except requests.exceptions.ConnectionError as e:
            logging.info(f"Proxy {self.proxies[0]} doesn't work. Try to use next proxy")
            self.proxies.pop(0)
            self.session.cookies.clear()
            return self.get_response(url, category, page)

    def parse_products(self, products: list):
        for product in products:
            if not product.get('title') \
                    or not product.get('code') \
                    or not product.get('id') \
                    or not product['metrics'].get('category') \
                    or not product.get('photos'):
                logging.exception(f"{config.MARKET}, can't find some keys. {product}")
                continue
            product_obj = {
                'name': product['title'],
                'url': f"https://www.mechta.kz/product/{product['code']}",
                'store_id': product['id'],
                'brand': product['metrics'].get('brand', None),
                'category': product['metrics']['category'],
                'images': ','.join(product['photos']),
            }
            product_obj = ProductSchema(**product_obj)
            price_obj = PriceSchema(price=product['prices']['discounted_price'])
            self.check_data_from_db(product_obj, price_obj)

    def check_data_from_db(self, product_obj: ProductSchema, price_obj: PriceSchema):
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
            all_prices: List[MechtaPrices] = self.prices_crud.get_last_n_prices(product.id)
            is_lowest_price = global_utils.check_lowest_price(price_obj.price, all_prices[1:], config.MARKET)
            is_in_stop_products_list = global_utils.is_in_stop_prdcts_list(product_obj.name)
            is_in_stop_categories_list = global_utils.is_in_stop_ctgrs_list(product_obj.category)
            if is_lowest_price and not is_in_stop_products_list and not is_in_stop_categories_list:
                all_prices_cleared = global_utils.clear_all_prices(all_prices)
                image_caption = utils.make_image_caption(product_obj, all_prices_cleared)
                try:
                    send_tg = send_to_tg.send_as_photo(
                        image_caption, product_obj.images.split(',')[0], global_config.TG_CHANNEL
                    )
                    if global_utils.is_in_pc_ctgrs_list(product_obj.category):
                        send_tg = send_to_tg.send_as_photo(
                            image_caption, product_obj.images.split(',')[0], global_config.TG_CHANNEL_PC
                        )
                    logging.info(f"TG status_code - {send_tg}. Product id - {product.id}")
                except:
                    return


if __name__ == '__main__':
    logging.basicConfig(
        handlers=[logging.FileHandler('../mechta_parser.log', 'a+', 'utf-8')],
        format="%(asctime)s %(levelname)s:%(message)s",
        level=logging.INFO,
    )
    MechtaParser().start()

import requests
import json
import logging
from random import randrange, shuffle
from time import sleep
from typing import List

from sulpak import categories, config, utils
from .schemas import ProductSchema, PriceSchema
from .models import SulpakPrices
from .crud import SulpakProductsCrud, SulpakPricesCrud
# from schemas import ProductSchema, PriceSchema
# from crud import SulpakProductsCrud, SulpakPricesCrud

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


class SulpakParser:
    def __init__(self):
        self.session = requests.session()
        self.db_session = SessionLocal()
        self.products_crud: SulpakProductsCrud = SulpakProductsCrud(session=self.db_session)
        self.prices_crud: SulpakPricesCrud = SulpakPricesCrud(session=self.db_session)
        self.proxies = Proxies().start()

    def start(self):
        logging.info(f"{config.MARKET} Parser Start")
        all_categories = categories.get_categories(self.session, self.proxies)
        shuffle(all_categories)
        for category in all_categories:
            page = 1
            try:
                response = self.get_response(f"{config.URL}/filter/goods", category, page)
            except:
                continue
            if not response:
                continue
            response = json.loads(response.text)
            total_product = response['total'] - config.LIMIT
            products = response['items']
            while total_product > 0:
                page += 1
                try:
                    append = self.get_response(f"{config.URL}/filter/goods", category, page)
                except:
                    continue
                if not append:
                    continue
                append = json.loads(append.text)
                products.extend(append['items'])
                total_product -= config.JSON_DATA['goodsPerPage']
            self.parse_products(products)
            sleep(randrange(global_config.SLEEP_START, global_config.SLEEP_FINISH))
        logging.info(f"{config.MARKET} Parser END")

    def get_response(self, url: str, category: dict, page: int) -> requests.models.Response | None:
        if not self.proxies:
            os.remove('../../proxies.json')
            self.session.cookies.clear()
            self.proxies = Proxies().start()
            return self.get_response(category, page)
        json_data = config.JSON_DATA
        json_data['classId'] = category['id']
        json_data['page'] = page
        try:
            response = self.session.post(url, headers=config.HEADER, json=json_data,
                                         proxies={'https': self.proxies[0]}, timeout=10)
            if response.status_code != 200:
                logging.info(f"Status code not 200 in proxy {self.proxies[0]}. Try to use next proxy")
                self.proxies.pop(0)
                self.session.cookies.clear()
                return self.get_response(url, category, page)
            return response
        except requests.exceptions.ConnectionError as e:
            logging.info(f"Proxy {self.proxies[0]} doesn't work. Try to use next proxy")
            self.proxies.pop(0)
            self.session.cookies.clear()
            return self.get_response(url, category, page)

    def parse_products(self, products: list):
        for product in products:
            if not product.get('fullTitle') \
                    or not product.get('slug') \
                    or not product.get('id') \
                    or not product.get('price') \
                    or not product.get('classTitle'): # \
                    # or not product.get('photoUrls'):
                # logging.error(f"{config.MARKET}, can't find some keys. {product}")
                continue
            img = product.get('photoUrls', global_config.FOR_MISSING_IMG)
            if img != global_config.FOR_MISSING_IMG:
                img = utils.make_image_url(img)
            product_obj = {
                'name': product['fullTitle'],
                'url': f"https://www.sulpak.kz/g/{product['slug']}",
                'store_id': product['id'],
                'brand': product.get('brand', ''),
                'category': product['classTitle'],
                'images': img,
                'characteristics': utils.make_characteristics(product.get('properties', []))
            }
            if not product_obj['brand']:
                product_obj['brand'] = ''
            product_obj = ProductSchema(**product_obj)
            price_obj = PriceSchema(price=product['price'])
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
            all_prices: List[SulpakPrices] = self.prices_crud.get_last_n_prices(product.id)
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
        handlers=[logging.FileHandler('sulpak_parser.log', 'a+', 'utf-8')],
        format="%(asctime)s %(levelname)s:%(message)s",
        level=logging.INFO,
    )
    SulpakParser().start()

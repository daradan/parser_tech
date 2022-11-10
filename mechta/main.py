import requests
import json
import logging

from mechta import categories, config, utils
from .schemas import ProductSchema, PriceSchema
from .crud import MechtaProductsCrud, MechtaPricesCrud

import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from database import SessionLocal
import send_to_tg


class MechtaParser:
    def __init__(self):
        self.session = requests.Session()
        self.db_session = SessionLocal()
        self.products_crud: MechtaProductsCrud = MechtaProductsCrud(session=self.db_session)
        self.prices_crud: MechtaPricesCrud = MechtaPricesCrud(session=self.db_session)
        self.items_count = 0

    def start(self):
        logging.info(f"{config.MARKET} Parser Start")
        try:
            for category in categories.get_categories(self.session):
                page = 1
                response = self.get_response(config.URL, category, page)
                total_product = response['all_items_count'] - response['page_items_count']
                products = response['items']
                logging.info(f'Finded {total_product} products in "{category}"')
                while total_product > 0:
                    page += 1
                    products.extend(self.get_response(config.URL, category, page)['items'])
                    total_product -= response['page_items_count']   # 24
                self.parse_products(products)
        except Exception as e:
            logging.exception(f"{config.MARKET}: {e}")
            send_to_tg.send_error(e)

    def get_response(self, url: str, category: str, page: int) -> json:
        params = config.PARAMS
        params['page'] = page
        params['section'] = category
        products = self.session.get(url, headers=config.HEADER, params=config.PARAMS).json()['data']
        product_ids = utils.get_product_ids(products['items'])

        data = config.DATA_1 + product_ids + config.DATA_2
        headers_prices = config.HEADERS_PRICES
        headers_prices['referer'] = f"{config.URL_REFERER}{category}/"
        prices = self.session.post(config.URL_PRICES, headers=headers_prices, data=data).json()['data']

        merged_products = utils.merge_price_to_products(products, prices)
        return merged_products

    def parse_products(self, products: list):
        for product in products:
            if not product.get('title') \
                    or not product.get('code') \
                    or not product.get('id') \
                    or not product['metrics'].get('brand') \
                    or not product['metrics'].get('category') \
                    or not product.get('photos'):
                continue
            product_obj = {
                'name': product['title'],
                'url': f"https://www.mechta.kz/product/{product['code']}",
                'store_id': product['id'],
                'brand': product['metrics']['brand'],
                'category': product['metrics']['category'],
                'images': ','.join(product['photos']),
            }
            product_obj = ProductSchema(**product_obj)
            price_obj = PriceSchema(price=product['prices']['discounted_price'])
            self.check_data_from_db(product_obj, price_obj)

    def check_data_from_db(self, product_obj: ProductSchema, price_obj: PriceSchema):
        self.items_count += 1
        logging.info(f"Check From DB: {self.items_count}")
        product = self.products_crud.get_or_create(product_obj)
        price_obj.product_id = product.id
        last_price = self.prices_crud.get_last_price(product.id)
        if last_price:
            discount = utils.get_percentage(price_obj.price, int(last_price.price))
            price_obj.discount = discount
        if not last_price or price_obj.discount != '0':
            self.prices_crud.insert(price_obj)
            logging.info(f"New Price: {price_obj.price} for product: {product.id}")
            if int(price_obj.discount) <= -15:
                image_caption = utils.make_image_caption(product_obj, self.prices_crud.get_last_n_prices(product.id))
                if len(product_obj.images.split(',')) > 1:
                    send_tg = send_to_tg.send_as_media_group(image_caption, product_obj)
                else:
                    send_tg = send_to_tg.send_as_photo(image_caption, product_obj.images)
                logging.info(f"Send to telegram status code: {send_tg}")


if __name__ == '__main__':
    logging.basicConfig(
        handlers=[logging.FileHandler('../mechta_parser.log', 'a+', 'utf-8')],
        format="%(asctime)s %(levelname)s:%(message)s",
        level=logging.INFO,
    )
    MechtaParser().start()

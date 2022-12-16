import requests
import json
import logging

from sulpak import categories, config, utils
from .schemas import ProductSchema, PriceSchema
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


class SulpakParser:
    def __init__(self):
        self.session = requests.session()
        self.db_session = SessionLocal()
        self.products_crud: SulpakProductsCrud = SulpakProductsCrud(session=self.db_session)
        self.prices_crud: SulpakPricesCrud = SulpakPricesCrud(session=self.db_session)
        self.items_count = 0

    def start(self):
        logging.info(f"{config.MARKET} Parser Start")
        for category in categories.get_categories(self.session):
            try:
                page = 1
                response = self.get_response(f"{config.URL}/filter/goods", category, page)
                total_product = response['total'] - config.JSON_DATA['goodsPerPage']
                products = response['items']
                logging.info(f'Finded {total_product} products in "{category}"')
                while total_product > 0:
                    page += 1
                    products.extend(self.get_response(f"{config.URL}/filter/goods", category, page)['items'])
                    total_product -= config.JSON_DATA['goodsPerPage']
                self.parse_products(products)
            except Exception as e:
                logging.exception(f"{config.MARKET} {category}: {e}")
                send_to_tg.send_error(f"{config.MARKET} {category}: {e}")
                continue

    def get_response(self, url: str, category: int, page: int) -> json:
        json_data = config.JSON_DATA
        json_data['classId'] = category
        json_data['page'] = page
        products = self.session.post(url, headers=config.HEADER, json=json_data).json()
        return products

    def parse_products(self, products: list):
        for product in products:
            try:
                if not product.get('fullTitle') \
                        or not product.get('code') \
                        or not product.get('slug') \
                        or not product.get('id') \
                        or not product.get('price') \
                        or not product.get('brand') \
                        or not product.get('classTitle') \
                        or not product.get('properties') \
                        or not product.get('photoUrls'):
                    continue
                product_obj = {
                    'name': product['fullTitle'],
                    'url': f"https://www.sulpak.kz/g/{product['slug']}",
                    'store_id': product['id'],
                    'brand': product['brand'],
                    'category': product['classTitle'],
                    'images': utils.make_image_url(product['photoUrls']),
                    'characteristics': utils.make_characteristics(product['properties'])
                }
                product_obj = ProductSchema(**product_obj)
                price_obj = PriceSchema(price=product['price'])
                self.check_data_from_db(product_obj, price_obj)
            except Exception as e:
                logging.exception(f"{config.MARKET} {product}: {e}")
                send_to_tg.send_error(f"{config.MARKET}: {e}")
                continue

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
                try:
                    if len(product_obj.images.split(',')) > 1:
                        send_tg = send_to_tg.send_as_media_group(image_caption, product_obj)
                    else:
                        send_tg = send_to_tg.send_as_photo(image_caption, product_obj.images)
                    logging.info(f"Send to telegram status code: {send_tg}")
                except Exception as e:
                    logging.exception(f"{config.MARKET} {image_caption}: {e}")
                    send_to_tg.send_error(f"{config.MARKET} {image_caption}: {e}")
                    return


if __name__ == '__main__':
    logging.basicConfig(
        handlers=[logging.FileHandler('sulpak_parser.log', 'a+', 'utf-8')],
        format="%(asctime)s %(levelname)s:%(message)s",
        level=logging.INFO,
    )
    SulpakParser().start()

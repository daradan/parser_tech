import requests
import json
import logging

from alser import categories, config, utils
from .schemas import ProductSchema, PriceSchema
from .crud import AlserProductsCrud, AlserPricesCrud

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


class AlserParser:
    def __init__(self):
        self.db_session = SessionLocal()
        self.session = requests.Session()
        self.products_crud: AlserProductsCrud = AlserProductsCrud(session=self.db_session)
        self.prices_crud: AlserPricesCrud = AlserPricesCrud(session=self.db_session)
        self.proxies = Proxies().start()

    def start(self):
        logging.info(f"{config.MARKET} Parser START")
        for category_id, category in categories.get_categories(self.session, self.proxies):
            try:
                page = 1
                response = self.get_response(int(category_id), page)
                total_product = response['_meta']['totalCount']
                products = response['data']
                logging.info(f'Finded {total_product} products in "{category_id}"')
                while page < response['_meta']['pageCount']:
                    page += 1
                    products.extend(self.get_response(category_id, page)['data'])
                self.parse_products(products, category)
            except Exception as e:
                logging.exception(f"{config.MARKET} {category}: {e}")
                send_to_tg.send_error(f"{config.MARKET} {category}: {e}")
                continue

    def get_response(self, category_id: int, page: int) -> json:
        json_data = config.JSON_DATA
        json_data['category_id'] = category_id
        json_data['page'] = page
        response = requests.post(f"{config.URL}/products", headers=config.HEADERS, json=json_data)
        if response.status_code != 200:
            self.get_response(category_id, page)
        return json.loads(response.text)

    def parse_products(self, products: list, category: str):
        for product in products:
            try:
                if not product.get('id') \
                        or not product.get('title') \
                        or not product.get('keyword') \
                        or not product.get('image') \
                        or not product.get('price') \
                        or not product.get('specs'):
                    continue
                if not product.get('specs') or len(product['specs']) <= 2 or not product['specs'][1].get('option_name'):
                    brand = ''
                else:
                    brand = product['specs'][1]['option_name']
                product_obj = {
                    'name': product['title'],
                    'url': f"{config.URL_P}/{product['keyword']}",
                    'store_id': product['id'],
                    'brand': brand,
                    'category': category,
                    'characteristics': utils.get_specs(product['specs']),
                    'images': utils.check_img(product['image']),
                }
                logging.info(f"product_obj: {product_obj}")
                product_obj = ProductSchema(**product_obj)
                price_obj = PriceSchema(price=int(product['price']))
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
        handlers=[logging.FileHandler('alser_parser.log', 'a+', 'utf-8')],
        format="%(asctime)s %(levelname)s:%(message)s",
        level=logging.INFO,
    )
    AlserParser().start()

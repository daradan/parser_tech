import requests
import json
import logging

from technodom import categories, config, utils, send_to_tg
from schemas import ProductSchema, PriceSchema
from crud import TechnodomProductsCrud, TechnodomPricesCrud
from database import SessionLocal


class TechnodomParser:
    def __init__(self):
        self.session = requests.Session()
        self.db_session = SessionLocal()
        self.products_crud: TechnodomProductsCrud = TechnodomProductsCrud(session=self.db_session)
        self.prices_crud: TechnodomPricesCrud = TechnodomPricesCrud(session=self.db_session)
        self.items_count = 0

    def start(self):
        logging.info('Technodom Parser Start')
        for catalog in categories.items:
            url = utils.make_url(catalog)
            page = 1
            response = self.get_response(url, page)
            total_product = response['total']
            products = response['payload']
            logging.info(f'Finded {total_product} products in "{catalog}"')
            while total_product > 0:
                page += 1
                products.extend(self.get_response(url, page)['payload'])
                total_product -= 24
            self.parse_products(products)

    def get_response(self, url: str, page: int) -> json:
        params = config.params
        params['page'] = page
        response = self.session.get(url, headers=config.headers, params=config.params)
        # logging.info(f'{url} - response {response.status_code}')
        return json.loads(response.text)

    def parse_products(self, products: list):
        for product in products:
            product_obj = {
                'name': product['title'],
                'url': f"https://www.technodom.kz/p/{product['uri']}",
                'brand': product['brand'],
                'category': product['categories_ru'][0],
                'is_new': product['is_new'],
                'color': product['color']['title'],
                'images': utils.make_images(product['images'])
            }
            product_obj = ProductSchema(**product_obj)
            price_obj = PriceSchema(price=int(product['price']))
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
        if not price_obj.discount:
            self.prices_crud.insert(price_obj)
            logging.info(f"New Price: {price_obj.price} for product: {product.id} - {product_obj.name}")
            return
        if price_obj.discount != '0':
            self.prices_crud.insert(price_obj)
            logging.info(f"Price changed: {price_obj.price} for product: {product.id} - {product_obj.name}")
            if int(price_obj.discount) <= -15:
                image_caption = utils.make_image_caption(product_obj, self.prices_crud.get_last_n_prices(product.id))
                send_tg = send_to_tg.send_as_photo(image_caption, product_obj.images.split(',')[0])
                logging.info(f"Send to telegram status code: {send_tg}")


if __name__ == '__main__':
    logging.basicConfig(
        handlers=[logging.FileHandler('technodom_parser.log', 'a+', 'utf-8')],
        format="%(asctime)s %(levelname)s:%(message)s",
        level=logging.INFO,
    )
    TechnodomParser().start()

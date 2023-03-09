import requests
import json
import re
import logging
from random import randrange, shuffle
from bs4 import BeautifulSoup
from time import sleep
from typing import List

from shop import categories, config, utils
from .schemas import ProductSchema, PriceSchema
from .models import ShopPrices
from .crud import ShopProductsCrud, ShopPricesCrud

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


class ShopParser:
    def __init__(self):
        self.session = requests.session()
        self.db_session = SessionLocal()
        self.products_crud: ShopProductsCrud = ShopProductsCrud(session=self.db_session)
        self.prices_crud: ShopPricesCrud = ShopPricesCrud(session=self.db_session)
        self.proxies = Proxies().start()

    def start(self):
        logging.info(f"{config.MARKET} Parser Start")
        all_categories_raw = categories.get_categories(self.session, self.proxies)
        all_categories = utils.make_cat_urls(all_categories_raw)
        shuffle(all_categories)
        for url_ctgr in all_categories:
            category_raw_items = []
            page = 1
            try:
                response = self.get_response(url_ctgr, page)
            except:
                continue
            if not response:
                continue
            items, next_page_link = self.get_soup(response)
            category_raw_items.extend(items)
            while next_page_link:
                page += 1
                response_next = self.get_response(url_ctgr, page)
                if not response_next:
                    continue
                items, next_page_link = self.get_soup(response_next)
                category_raw_items.extend(items)
            self.parse_items(category_raw_items)
            sleep(randrange(global_config.SLEEP_START, global_config.SLEEP_FINISH))
        logging.info(f"{config.MARKET} Parser END")

    def get_response(self, url: str, page: int) -> requests.models.Response | None:
        if not self.proxies:
            os.remove('../../proxies.json')
            self.session.cookies.clear()
            proxies = Proxies().start()
            return self.get_response(url, page)
        params = {'PAGEN_1': page}
        try:
            response = self.session.get(url=url, headers=config.HEADERS, params=params, cookies=config.COOKIES,
                                        proxies={'https': self.proxies[0]}, timeout=10)
            if response.status_code != 200:
                logging.info(f"Status code not 200 in proxy {self.proxies[0]}. Try to use next proxy")
                self.proxies.pop(0)
                self.session.cookies.clear()
                return self.get_response(url, page)
        except requests.exceptions.ConnectionError as e:
            logging.info(f"Proxy {self.proxies[0]} doesn't work. Try to use next proxy")
            self.proxies.pop(0)
            self.session.cookies.clear()
            return self.get_response(url, page)
        return response

    def get_soup(self, response: requests.models.Response) -> tuple:
        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.find_all('div', class_='bx_catalog_item')
        try:
            next_page_link = soup.find('li', class_='bx-pag-next').a
        except AttributeError:
            return items, None
        return items, next_page_link

    def parse_items(self, items: list):
        for item in items:
            try:
                # some_info = json.loads(
                #     item.find('div', class_='bx_catalog_item_container gtm-impression-product').get('data-product')
                # )
                some_info = item.find('div', class_='bx_catalog_item_container gtm-impression-product').\
                    get('data-product')
                # some_info = re.sub('(" \w)', ', ', some_info)
                some_info = re.sub('(", \w)', ', ', some_info)
                some_info = json.loads(some_info)
                url = item.find('div', class_='bx_catalog_item_title').a.get('href')

                item_prop = item.find_all('span', class_='bx_catalog_item_prop')
                item_value = item.find_all('span', class_='bx_catalog_item_value')
                characteristics_list = []
                for prop, value in zip(item_prop, item_value):
                    characteristics_list.append(f"{prop.text} {value.text}")
                image = item.find('img').get('data-src')
                # price = item.find_all('span', class_='bx-more-price-text')[-1].text
                price = ''
                for price_title in item.find_all(attrs={'class': 'bx-more-price-title'}):
                    if price_title.text == 'Цена в интернет-магазине':
                        price = price_title.next_sibling.text
                        break
                price = ''.join([k for k in price.split() if k.isdigit()])
                # price = int(some_info.get('item_id'))
                if not price:
                    continue
            except Exception as e:
                logging.error(f"{config.MARKET}, can't find some keys. {e}\n{item}")
                continue

            product_obj = {
                'name': some_info.get('item_name'),
                'url': config.URL + url,
                'store_id': some_info.get('item_id'),
                'brand': str(some_info.get('item_brand', '')),
                'category': some_info.get('item_category'),
                'images': 'https:' + image,
                'characteristics': '\n'.join(characteristics_list),
            }
            product_obj = ProductSchema(**product_obj)
            price_obj = PriceSchema(price=price)
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
            all_prices: List[ShopPrices] = self.prices_crud.get_last_n_prices(product.id)
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
        handlers=[logging.FileHandler('shop_parser.log', 'a+', 'utf-8')],
        format="%(asctime)s %(levelname)s:%(message)s",
        level=logging.INFO,
    )
    ShopParser().start()

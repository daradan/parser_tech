import json
import requests
import logging
import re
import string
from random import randrange, shuffle, choices
from bs4 import BeautifulSoup, ResultSet
from time import sleep
from typing import List
from pydantic import ValidationError

from dns import categories, config, utils
from .schemas import ProductSchema, PriceSchema
from .models import DnsPrices
from .crud import DnsProductsCrud, DnsPricesCrud

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


class DnsParser:
    def __init__(self):
        self.session = requests.session()
        self.db_session = SessionLocal()
        self.products_crud: DnsProductsCrud = DnsProductsCrud(session=self.db_session)
        self.prices_crud: DnsPricesCrud = DnsPricesCrud(session=self.db_session)
        # self.count = 0
        self.proxies = Proxies().start()

    def start(self):
        logging.info(f"{config.MARKET} Parser Start")
        all_categories = categories.get_categories(self.session, self.proxies)
        shuffle(all_categories)
        for category in all_categories:
            category_raw_items = []
            raw_items, category_name, next_page = self.get_items(category['url'])
            if not raw_items:
                continue
            category_raw_items += raw_items
            prices = self.get_prices(category_raw_items)
            if not prices:
                continue
            while next_page:
                raw_items, category_name, next_page = self.get_items(next_page)
                if not raw_items:
                    continue
                category_raw_items += raw_items
                prices = self.get_prices(category_raw_items)
                if not prices:
                    continue
            self.parse_items(category_raw_items, category_name, prices)
            sleep(randrange(global_config.SLEEP_START, global_config.SLEEP_FINISH))
        logging.info(f"{config.MARKET} Parser END")

    def get_items(self, url: str) -> tuple[List[ResultSet], str, str | None] | tuple[None, None, None]:
        if not self.proxies:
            os.remove('../../proxies.json')
            self.session.cookies.clear()
            self.proxies = Proxies().start()
            return self.get_items(url)
        try:
            response = self.session.get(
                url, headers=config.HEADERS, cookies=config.COOKIE,
                proxies={'https': f"{self.proxies[0]}"}, timeout=10
            )
            if response.status_code != 200:
                logging.info(f"Status code not 200 in proxy {self.proxies[0]}. Try to use next proxy")
                self.proxies.pop(0)
                self.session.cookies.clear()
                return self.get_items(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            raw_items = soup.find_all('div', class_='catalog-product ui-button-widget')
            category_name = soup.find('h1', class_='title').text
            next_page = soup.find(attrs={'class': 'pagination-widget__page-link_next'}).get('href')
            if next_page == 'javascript:':
                return raw_items, category_name, None
            next_page_link = config.URL + next_page
        except requests.exceptions.ConnectionError as e:
            logging.info(f"Proxy {self.proxies[0]} doesn't work. Try to use next proxy")
            self.proxies.pop(0)
            self.session.cookies.clear()
            return self.get_items(url)
        except AttributeError as e:
            logging.error(f'AttributeError - {e}')
            if not raw_items:
                return None, None, None
            return raw_items, category_name, None
        except Exception as e:
            logging.error(f'Exception - {e}')
            return None, None, None
        return raw_items, category_name, next_page_link

    def get_prices(self, items: List[ResultSet]) -> dict | None:
        containers = []
        prices = []
        for_price = []
        for item in items:
            random_id = 'as_' + ''.join(choices(string.ascii_letters, k=6))
            data_id = {'id': item.get('data-product')}
            for_price.append(item.get('data-product'))
            containers.append({'id': random_id, 'data': data_id})
        data = 'data={"type":"product-buy","containers":[' + ','.join(map(str,containers)) + ']}'
        data = data.replace(' ', '')
        data = data.replace('\'', '"')
        try:
            response = self.session.post(
                config.URL_P, params=config.PARAMS_P, headers=config.HEADERS_P, data=data, verify=False,
                proxies={'https': f"{self.proxies[0]}"}, timeout=10
            )
            prices_json = json.loads(response.text)['data']['states']
        except requests.exceptions.ConnectionError as e:
            logging.error(f'ConnectionError - {e}')
            self.proxies.pop(0)
            self.session.cookies.clear()
            return self.get_prices(items)
        except Exception as e:
            return
        for price in prices_json:
            prices.append(price['data']['price']['current'])
        return dict(zip(for_price, prices))

    def parse_items(self, items: list, category: str, prices: dict):
        for item in items:
            try:
                name: str = item.find(attrs={'class': 'catalog-product__name'}).text
                url: str = item.find(attrs={'class': 'catalog-product__name'}).get('href')
                image: str = item.find(attrs={'type': 'image/webp'}).get('data-srcset')
                if not image:
                    image = global_config.FOR_MISSING_IMG
                price = prices[item.get('data-product')]
                try:
                    characteristics: str = re.search(r'\[(.*?)\]', name).group(1).replace(', ', '\n')
                except AttributeError as e:
                    characteristics = ''
                store_id = item.get('data-code')
                store_code = item.get('data-product')

                product_obj = {
                    'name': name.split('[')[0],
                    'url': config.URL + url,
                    'store_id': store_id,
                    'store_code': store_code,
                    'category': category,
                    'images': image,
                    'characteristics': characteristics,
                }
                product_obj = ProductSchema(**product_obj)
                price_obj = PriceSchema(price=price)
                self.check_data_from_db(product_obj, price_obj)
            except ValidationError as e:
                logging.error(f"{config.MARKET}, pydantic ValidationError - {e}\nCategory is - {category}\n{item}")
                continue
            except Exception as e:
                logging.error(f"{config.MARKET}, can't find some keys. {e}\n{item}")
                continue

    def check_data_from_db(self, product_obj: ProductSchema, price_obj: PriceSchema) -> None:
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
            all_prices: List[DnsPrices] = self.prices_crud.get_all_prices(product.id)
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
        handlers=[logging.FileHandler('dns_parser.log', 'a+', 'utf-8')],
        format="%(asctime)s %(levelname)s:%(message)s",
        level=logging.INFO,
    )
    DnsParser().start()

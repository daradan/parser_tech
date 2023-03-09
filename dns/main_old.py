# import requests
# import logging
# import re
# from random import randrange, shuffle, choices
# from playwright.sync_api import sync_playwright, TimeoutError, Page
# from bs4 import BeautifulSoup, ResultSet
# from time import sleep
# from typing import List
#
# from dns import categories, config, utils
# from .schemas import ProductSchema, PriceSchema
# from .models import DnsPrices
# from .crud import DnsProductsCrud, DnsPricesCrud
#
# import sys
# import os
# current = os.path.dirname(os.path.realpath(__file__))
# parent = os.path.dirname(current)
# sys.path.append(parent)
# from database import SessionLocal
# import send_to_tg
# import global_utils
# import global_config
#
#
# class DnsParser:
#     def __init__(self):
#         self.session = requests.session()
#         self.db_session = SessionLocal()
#         self.products_crud: DnsProductsCrud = DnsProductsCrud(session=self.db_session)
#         self.prices_crud: DnsPricesCrud = DnsPricesCrud(session=self.db_session)
#         self.count = 0
#
#     def start(self):
#         logging.info(f"{config.MARKET} Parser Start")
#         all_categories = categories.get_categories(self.session)
#         shuffle(all_categories)
#         for category in all_categories:
#         with sync_playwright() as pw:
#             browser = pw.chromium.launch(headless=False)
#             context = browser.new_context()
#             context.add_cookies(config.COOKIES)
#             page = context.new_page()
#             for category in all_categories:
#                 items_raw = []
#                 try:
#                     response, category_name = self.get_response(category['url'], page)
#                 except:
#                     continue
#                 if not response:
#                     continue
#                 items, next_page_link = self.get_soup(response)
#                 items_raw.extend(items)
#                 while next_page_link:
#                     response_next, category_name = self.get_response(next_page_link, page)
#                     if not response_next:
#                         continue
#                     items, next_page_link = self.get_soup(response_next)
#                     items_raw.extend(items)
#                 self.parse_items(items_raw, category_name)
#                 # sleep(randrange(global_config.SLEEP_START, global_config.SLEEP_FINISH))
#         logging.info(f"{config.MARKET} Parser END")
#
#     def get_response(self, category: str, page: Page) -> tuple[str, str] | tuple[None, None]:
#         try:
#             response = page.goto(category)
#         except TimeoutError as e:
#             logging.error(f'Exception - {e}')
#             return None, None
#         if not response.ok:
#             logging.error(f'Response - {response.status}')
#             return None, None
#         page.wait_for_selector('div[class=products-page__list]')
#         category_name = page.inner_html('h1.title')
#         return page.inner_html('div.products-page__list'), category_name
#
#     def get_soup(self, response_text: str) -> tuple:
#         soup = BeautifulSoup(response_text, 'html.parser')
#         items = soup.find_all(attrs={'class': 'catalog-product'})
#         try:
#             next = soup.find(attrs={'class': 'pagination-widget__page-link_next'}).get('href')
#             if next == 'javascript:':
#                 return items, None
#             next_page_link = config.URL + next
#         except AttributeError:
#             return items, None
#         return items, next_page_link
#
#     def parse_items(self, items: list, category: str):
#         for item in items:
#             try:
#                 name: str = item.find(attrs={'class': 'catalog-product__name'}).text
#                 url: str = item.find(attrs={'class': 'catalog-product__name'}).get('href')
#                 image = item.find(attrs={'type': 'image/webp'}).get('data-srcset')
#                 if not image:
#                     image = global_config.FOR_MISSING_IMG
#                 price = item.find('div', class_='product-buy__price').text.split('₸')[0]
#                 price = ''.join([k for k in price.split() if k.isdigit()])
#                 characteristics: str = re.search(r'\[(.*?)\]', name).group(1).replace(', ', '\n')
#                 store_id = item.get('data-code')
#                 store_code = item.get('data-product')
#             except Exception as e:
#                 logging.error(f"{config.MARKET}, can't find some keys. {e}\n{item}")
#                 continue
#
#             product_obj = {
#                 'name': name.split('[')[0],
#                 'url': config.URL + url,
#                 'store_id': store_id,
#                 'store_code': store_code,
#                 'category': category,
#                 'images': image,
#                 'characteristics': characteristics,
#             }
#             product_obj = ProductSchema(**product_obj)
#             price_obj = PriceSchema(price=price)
#             self.check_data_from_db(product_obj, price_obj)
#
#     def check_data_from_db(self, product_obj: ProductSchema, price_obj: PriceSchema):
#         product = self.products_crud.get_or_create(product_obj)
#         price_obj.product_id = product.id
#         last_price = self.prices_crud.get_last_price(product.id)
#         if last_price:
#             discount = global_utils.get_percentage(price_obj.price, int(last_price.price))
#             price_obj.discount = discount
#         if not last_price or price_obj.discount != '0':
#             self.prices_crud.insert(price_obj)
#             if not last_price:
#                 return
#             all_prices: List[DnsPrices] = self.prices_crud.get_all_prices(product.id)
#             is_lowest_price = global_utils.check_lowest_price(price_obj.price, all_prices[1:], config.MARKET)
#             is_in_stop_products_list = global_utils.is_in_stop_prdcts_list(product_obj.name)
#             is_in_stop_categories_list = global_utils.is_in_stop_ctgrs_list(product_obj.category)
#             if is_lowest_price and not is_in_stop_products_list and not is_in_stop_categories_list:
#                 all_prices_cleared = global_utils.clear_all_prices(all_prices)
#                 image_caption = utils.make_image_caption(product_obj, all_prices_cleared)
#                 try:
#                     send_tg = send_to_tg.send_as_photo(image_caption, product_obj.images.split(',')[0])
#                     logging.info(f"TG status_code - {send_tg}. Product id - {product.id}")
#                 except:
#                     return
#
#
# if __name__ == '__main__':
#     logging.basicConfig(
#         handlers=[logging.FileHandler('dns_parser.log', 'a+', 'utf-8')],
#         format="%(asctime)s %(levelname)s:%(message)s",
#         level=logging.INFO,
#     )
#     DnsParser().start()
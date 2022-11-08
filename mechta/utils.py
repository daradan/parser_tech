from . import config
import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import global_config

# from dotenv import load_dotenv, find_dotenv
#
# load_dotenv(find_dotenv())


def make_url(catalog: str) -> str:
    url = f"{config.URL}{catalog}"
    return url


def get_product_ids(products_items: list) -> str:
    product_ids = []
    for product in products_items:
        product_ids.append(str(product['id']))
    return ','.join(product_ids)


def merge_price_to_products(products: dict, prices: dict) -> dict:
    for key, value in prices.items():
        for num, prdct_value in enumerate(products['items']):
            if value['id'] == prdct_value['id']:
                products['items'][num].update(value)
    return products


def get_percentage(price, price_old):
    percent = round(-1 * (100 - (price * 100 / price_old)))
    if percent > 0:
        percent = f'+{percent}'
    return str(percent)


def make_image_caption(product_obj, last_n_prices):
    fixed_category = fix_category(product_obj.category)
    image_caption = f"<b>{product_obj.name}</b>\n" \
                    f"#{config.MARKET} #{fixed_category} #{product_obj.brand}\n\n" \
                    f"{fix_last_n_prices(last_n_prices)}\n" \
                    f"<a href='{product_obj.url}{make_utm_tags()}'>Купить на оф.сайте</a>\n\n" \
                    f"{global_config.TG_CHANNEL}"
    return image_caption


def fix_category(category):
    need_to_replace = [' ', '-']
    for change in need_to_replace:
        if change in category:
            category = category.replace(change, '_')
    return category


def fix_last_n_prices(last_n_prices):
    last_n_prices_text = ''
    for data_price in last_n_prices:
        if data_price.discount:
            dscnt = f' ({data_price.discount}%)'
        else:
            dscnt = ''
        last_n_prices_text += f'{data_price.created.year}/{data_price.created.month}/{data_price.created.day}' \
                              f' - {data_price.price} ₸{dscnt}\n'
    return last_n_prices_text


def make_utm_tags() -> str:
    utm_campaign = global_config.TG_CHANNEL[1:]
    return f"?utm_source=telegram&utm_medium=messenger&utm_campaign={utm_campaign}&utm_term={global_config.TG_CHANNEL_NAME}"

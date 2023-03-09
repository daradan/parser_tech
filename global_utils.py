from typing import List

# from global_config import STOP_PRODUCTS_LIST, STOP_CATEGORIES_LIST, MIN_PRICE, PERCENTAGE
import global_config
from technodom.models import TechnodomPrices
from mechta.models import MechtaPrices
from sulpak.models import SulpakPrices
from alser.models import AlserPrices


def get_percentage(price: int, price_old: int) -> str:
    percent = round(-1 * (100 - (price * 100 / price_old)))
    if percent > 0:
        percent = f'+{percent}'
    return str(percent)


def get_model(market: str):
    if market.lower() == 'technodom':
        return TechnodomPrices
    if market.lower() == 'mechta':
        return MechtaPrices
    if market.lower() == 'sulpak':
        return SulpakPrices
    if market.lower() == 'alser':
        return AlserPrices


def check_lowest_price(price: int, last_n_prices, market) -> bool:
    last_n_prices: List[get_model(market)] = last_n_prices
    prices_list = []
    for data_price in last_n_prices:
        prices_list.append(int(data_price.price))
    price_diff = min(prices_list) - (min(prices_list) * global_config.PERCENTAGE / 100)
    if min(prices_list) > price > global_config.MIN_PRICE and price_diff > price:
        return True
    return False


def is_in_stop_prdcts_list(product_name: str) -> bool:
    for stop_product in global_config.STOP_PRODUCTS_LIST:
        if stop_product.lower() in product_name.lower():
            return True
    return False


def is_in_stop_ctgrs_list(category: str) -> bool:
    for stop_category in global_config.STOP_CATEGORIES_LIST:
        if category == stop_category:
            return True
    return False


def is_in_pc_ctgrs_list(category: str) -> bool:
    if category in global_config.PC_CATEGORY:
        return True
    return False


def clear_all_prices(all_prices: list) -> list:
    if len(all_prices) <= 2:
        return all_prices
    all_prices_cleared = []
    for price in all_prices:
        if int(price.discount) == 0 \
                or not(global_config.PERCENTAGE_BELOW <= int(price.discount) <= global_config.PERCENTAGE_ABOVE):
            all_prices_cleared.append(price)
    while len(all_prices_cleared) > global_config.LAST_N_PRICES:
        # all_prices_cleared.pop(-2)
        all_prices_cleared.pop()
    return all_prices_cleared


def fix_category(category: str) -> str:
    # if ' / ' in category:
    #     return ' #'.join(category.split(' / '))

    def fix_category2(category2: str) -> str:
        need_to_replace = [' & ', ' ', '-', '+']
        for change in need_to_replace:
            if change in category2:
                category2 = category2.replace(change, '_')
        return category2

    def fix_category3(category3: str, symbol: str) -> str:
        temp = []
        temp_list = category3.split(symbol)
        for text in temp_list:
            temp.append(fix_category2(text))
        return ' #'.join(temp)

    if ',' in category:
        return fix_category3(category, ',')
    if ' / ' in category:
        return fix_category3(category, ' / ')

    # if ' & ' in category:
    #     temp = []
    #     temp_list = category.split(' & ')
    #     for text in temp_list:
    #         temp.append(fix_category2(text))
    #     return ' #'.join(temp)
    return fix_category2(category)


def fix_all_prices(all_prices: list) -> str:
    all_prices_text = ''
    for data_price in all_prices:
        month = data_price.created.month
        day = data_price.created.day
        if data_price.discount:
            dscnt = f' ({data_price.discount}%)'
        else:
            dscnt = ''
        if month < 10:
            month = f"0{month}"
        if day < 10:
            day = f"0{day}"
        all_prices_text += f'{data_price.created.year}/{month}/{day} - {data_price.price} ₸{dscnt}\n'
    return all_prices_text


def make_utm_tags() -> str:
    utm_campaign = global_config.TG_CHANNEL[1:]
    return f"?utm_source=telegram&utm_medium=messenger&utm_campaign=" \
           f"{utm_campaign}&utm_term={global_config.TG_CHANNEL_NAME}"

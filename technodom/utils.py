import config
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


def make_url(catalog: str) -> str:
    url = f"{config.url_td}{catalog}"
    return url


def make_images(images: list) -> str:
    img_lst = []
    for image in images:
        img_lst.append(f"https://api.technodom.kz/f3/api/v1/images/1080/1080/{image}.jpg")
    return ','.join(img_lst)


def get_percentage(price, price_old):
    percent = round(-1 * (100 - (price * 100 / price_old)))
    if percent > 0:
        percent = f'+{percent}'
    return str(percent)


def make_image_caption(product_obj, last_n_prices):
    fixed_category = fix_category(product_obj.category)
    image_caption = f"<b>{product_obj.name}</b>\n" \
                    f"<b>{product_obj.color}</b>\n" \
                    f"#Technodom #{fixed_category} #{product_obj.brand}\n\n" \
                    f"{fix_last_n_prices(last_n_prices)}\n" \
                    f"<a href='{product_obj.url}'>Купить на оф.сайте</a>\n\n" \
                    f"{os.getenv('TG_CHANNEL')}"
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

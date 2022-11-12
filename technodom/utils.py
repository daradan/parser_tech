from . import config
import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import global_config


def make_url(catalog: str) -> str:
    url = f"{config.URL}{catalog}"
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
                    f"#{config.MARKET} #{fixed_category} #{fix_category(product_obj.brand)}\n\n" \
                    f"{fix_last_n_prices(last_n_prices)}\n" \
                    f"<a href='{product_obj.url}{make_utm_tags()}'>Купить на оф.сайте</a>\n\n" \
                    f"{global_config.TG_CHANNEL}"
    return image_caption


def fix_category(category):
    need_to_replace = [' ', '-', ',']
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

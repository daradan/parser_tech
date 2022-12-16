import time
import requests
import json
import logging

import global_config


def send_error(message):
    url = f'https://api.telegram.org/bot{global_config.TG_TOKEN}/sendMessage'
    params = {
        'chat_id': global_config.TG_CHANNEL_ERROR,
        'text': message
    }
    r = requests.post(url, data=params)
    if r.status_code != 200:
        data = r.json()
        logging.info(f"TG ERROR: {data}")
        time_to_sleep = data['parameters']['retry_after']
        time.sleep(time_to_sleep)
        send_error(message)
        return r.status_code


def send_msg(message):
    url = f'https://api.telegram.org/bot{global_config.TG_TOKEN}/sendMessage'
    params = {
        'chat_id': global_config.TG_CHANNEL,
        'text': message,
        'parse_mode': 'HTML'
    }
    r = requests.post(url, data=params)
    if r.status_code != 200:
        data = r.json()
        logging.info(f"TG MSG: {data}")
        time_to_sleep = data['parameters']['retry_after']
        time.sleep(time_to_sleep)
        send_error(message)
        return r.status_code


def send_as_photo(image_caption, image):
    url = f'https://api.telegram.org/bot{global_config.TG_TOKEN}/sendPhoto'
    params = {
        'chat_id': global_config.TG_CHANNEL,
        'caption': image_caption,
        'parse_mode': 'HTML',
        'photo': image,
    }
    r = requests.post(url, data=params)
    if r.status_code != 200:
        data = r.json()
        logging.info(f"TG PHOTO: {data}")
        if data['error_code'] == 400:
            send_msg(image_caption)
            return r.status_code
        time_to_sleep = data['parameters']['retry_after']
        time.sleep(time_to_sleep)
        send_as_photo(image_caption, image)
        return r.status_code


def send_as_media_group(image_caption, product):
    url = f'https://api.telegram.org/bot{global_config.TG_TOKEN}/sendMediaGroup'
    params = {
        'chat_id': global_config.TG_CHANNEL,
        'media': [],
    }
    for path in product.images.split(',')[:2]:
        params['media'].append({'type': 'photo',
                                'media': path,
                                'parse_mode': 'HTML', })
    params['media'][0]['caption'] = image_caption
    params['media'] = json.dumps(params['media'])
    r = requests.post(url, data=params)
    if r.status_code != 200:
        data = r.json()
        logging.info(f"TG MEDIA_G: {data}")
        if data['error_code'] == 400:
            send_msg(image_caption)
            return r.status_code
        time_to_sleep = data['parameters']['retry_after']
        time.sleep(time_to_sleep)
        send_as_media_group(image_caption, product)
        return r.status_code

import time
import requests
import json
import logging

import global_config

count = 0


def send_error(message: str) -> int:
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
        return send_error(message)
    return r.status_code


def send_msg(message: str, channel: str) -> int:
    url = f'https://api.telegram.org/bot{global_config.TG_TOKEN}/sendMessage'
    params = {
        'chat_id': channel,
        'text': message,
        'parse_mode': 'HTML'
    }
    r = requests.post(url, data=params)
    if r.status_code != 200:
        data = r.json()
        logging.info(f"TG MSG: {data}\nMessage is: {message}")
        time_to_sleep = data['parameters']['retry_after']
        time.sleep(time_to_sleep)
        return send_error(message)
    return r.status_code


def send_as_photo(image_caption: str, image: str, channel: str) -> int:
    global count
    url = f'https://api.telegram.org/bot{global_config.TG_TOKEN}/sendPhoto'
    params = {
        'chat_id': channel,
        'caption': image_caption,
        'parse_mode': 'HTML',
        'photo': image,
    }
    r = requests.post(url, data=params)
    if r.status_code != 200:
        data = r.json()
        logging.info(f"ERROR: TG PHOTO: {data}\nCaption is: {image_caption}")
        if data['error_code'] == 400:
            return send_msg(image_caption, channel)
        time_to_sleep = data['parameters']['retry_after']
        time.sleep(time_to_sleep)
        return send_as_photo(image_caption, image, channel)
    return r.status_code


def send_as_media_group(image_caption: str, product, channel: str) -> int:
    url = f'https://api.telegram.org/bot{global_config.TG_TOKEN}/sendMediaGroup'
    params = {
        'chat_id': channel,
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
            send_msg(image_caption, channel)
        time_to_sleep = data['parameters']['retry_after']
        time.sleep(time_to_sleep)
        return send_as_media_group(image_caption, product, channel)
    return r.status_code

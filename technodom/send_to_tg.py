import requests
import json
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
tg_token = os.getenv('TG_TOKEN')
tg_channel = os.getenv('TG_CHANNEL')
url_part = f"https://api.telegram.org/bot{tg_token}/"


def send_as_photo(msg: str, media: str):
    url = f'{url_part}sendPhoto'
    params = {
        'chat_id': tg_channel,
        'caption': msg,
        'parse_mode': 'HTML',
        'photo': media,
    }
    r = requests.post(url, data=params)
    return r.status_code


def send_as_media_group(msg: str, media: str):
    url = f'{url_part}sendMediaGroup'
    params = {
        'chat_id': tg_channel,
        'media': [],
    }
    media = list(media.split(', '))
    for path in media:
        params['media'].append({'type': 'photo',
                                'media': path,
                                'parse_mode': 'HTML', })
    params['media'][0]['caption'] = msg
    params['media'] = json.dumps(params['media'])
    r = requests.post(url, data=params)
    return r.status_code

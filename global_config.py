import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

LAST_N_PRICES = 10
TG_TOKEN = os.getenv('TG_TOKEN')
TG_CHANNEL = os.getenv('TG_CHANNEL')
TG_CHANNEL_ERROR = os.getenv('TG_CHANNEL_ERROR')
TG_CHANNEL_NAME = 'technics_discount_in_kazakhstan'

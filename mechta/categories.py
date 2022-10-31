import requests
from . import config

# items = ['telefony-eed', 'planshety-noutbuki-kompyutery', 'igry-konsoli-i-razvlecheniya', 'televizory-audio-video',
#          'tehnika-dlya-doma', 'klimat-tehnika', 'krasota-i-zdorove', 'kuhonnaya-tehnika', 'vstraivaemaya-tehnika',
#          'posuda-i-aksessuary', 'foto-videokamery-optika', 'aktivnyy-otdyh', 'avtoaksessuary', 'novogodnie-tovary']


def get_categories(session):
    categories = []
    data = session.get(config.URL_CATEGORY, headers=config.HEADER).json()
    for category in data['data']['menu_catalog'].values():
        categories.append(category['code'])
    return categories


if __name__ == '__main__':
    session = requests.session()
    print(get_categories(session))

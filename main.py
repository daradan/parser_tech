import logging
from logging.handlers import RotatingFileHandler
from random import shuffle

import technodom
import mechta
import sulpak
import alser
import shop
import dns


if __name__ == '__main__':
    logging.basicConfig(
        handlers=[RotatingFileHandler('parser_tech.log', mode='a+', maxBytes=10485760, backupCount=2, encoding='utf-8')],
        format="%(asctime)s %(levelname)s:%(message)s",
        level=logging.INFO,
    )

parsers = [
    technodom.TechnodomParser().start,
    mechta.MechtaParser().start,
    sulpak.SulpakParser().start,
    # alser.AlserParser().start,
    shop.ShopParser().start,
    dns.DnsParser().start,
]
shuffle(parsers)
for parser in parsers:
    parser()

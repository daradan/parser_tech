import logging
from logging.handlers import RotatingFileHandler
import technodom
import mechta
import sulpak

if __name__ == '__main__':
    logging.basicConfig(
        handlers=[RotatingFileHandler('parser_tech.log', mode='a+', maxBytes=10485760, backupCount=2, encoding='utf-8')],
        format="%(asctime)s %(levelname)s:%(message)s",
        level=logging.INFO,
    )

    technodom.TechnodomParser().start()
    mechta.MechtaParser().start()
    sulpak.SulpakParser().start()

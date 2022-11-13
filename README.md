## Скрейпинг магазинов электробытовой и компьютерной техники Казахстана
Скрипт скрейпит (парсит) сайты и добавляет в БД информацию о товаре. При следующем запуске проверяет продукт, и в случае изменения цены добавляет новую цену в БД. Если цена снизилась на <= 15%, то отправляет на Telegram-канал.

Источники:
- [x] technodom
- [x] mechta
- [x] sulpak
- [ ] dns-shop
- [ ] shop
- [ ] alser

### Установка и настройка
Клонируем репозитории
```
git clone https://github.com/daradan/parser_tech.git
```
Устанавливаем библиотеки
```
pip install -r requirements.txt
```
Создаем файл ___.env___ и заполняем свои данные
```
TG_TOKEN=...
TG_CHANNEL=...
TG_CHANNEL_ERROR=...
SULPAK_AUTH=...
```
**В SULPAK_AUTH добавляем Bearer Token*
## Scraping stores of household appliances and computer equipment in Kazakhstan
The script scrapes (parses) the sites and adds information about the product to the database. At the next launch it checks the product, and if the price has changed, adds a new price to the database. If the price has dropped by <= 15%, it sends to the Telegram feed.

Sources:
- [x] technodom
- [x] mechta
- [x] sulpak
- [ ] dns-shop
- [ ] shop
- [ ] alser

### Installation and setup
Clone repositories
```
git clone https://github.com/daradan/parser_tech.git
```
Installing libraries
```
pip install -r requirements.txt
```
Create file ___.env___ and fill in your data
```
TG_TOKEN=...
TG_CHANNEL=...
TG_CHANNEL_ERROR=...
SULPAK_AUTH=...
```
**Add Bearer Token to SULPAK_AUTH*
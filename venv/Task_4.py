"""
1.	Написать приложение, которое собирает основные новости с сайта на выбор news.mail.ru, lenta.ru, yandex-новости.
 Для парсинга использовать XPath. Структура данных должна содержать:
o	название источника;
o	наименование новости;
o	ссылку на новость;
o	дата публикации.
2.	Сложить собранные новости в БД
Минимум один сайт, максимум - все три
"""

from lxml import html
import requests
from pprint import pprint
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)  # подключаюсь к серверу баз данных mongo
db = client['news3005']  # создаю базу данных 'news3005'
headers = {'user-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                         ' AppleWebKit/537.36 (KHTML, like Gecko)'
                         ' Chrome/101.0.4951.67 Safari/537.36'}
link = 'https://lenta.ru/'

response = requests.get(link)

dom = html.fromstring(response.text)
items = dom.xpath("//a[contains(@class, '_topnews')]")  # все основные новости

list_items = []
for item in items:
    item_info = {}
    # среди главный новостей есть самая главная ('big') и остальные ('mini'): находим наименование новости
    name = item.xpath(".//span[contains(@class='card-big__title' and contains(@class='card-mini__title']/text()")[0]
    link = item.xpath("./@href")  # ссылка на новость
    date = item.xpath(".//time[contains(@class,'date']/text()")[0]  # дата новости
    # ссылка на источник новости находится в самой новости
    news_source = item.xpath("./@href")  # источник новости

    item_info['name'] = name
    item_info['link'] = link[0]
    item_info['date'] = date
    item_info['news_source'] = news_source[1]
    list_items.append(item_info)

pprint(list_items)

db.news3005.insertOne(list_items)  # складываю собранные новости в БД



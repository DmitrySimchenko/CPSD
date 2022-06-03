''' Написать программу, которая собирает товары «В тренде» с сайта техники mvideo и складывает данные в БД.
Сайт можно выбрать и свой. Главный критерий выбора: динамически загружаемые товары.
'''

from pprint import pprint
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select  # тег для работы с полями выбора
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
db = client['base_mvideo']
trends_db = db.mvideo_trends

s = Service('./chromedriver')
options = Options()  # формируем опции запуска
options.add_argument('start-maximized')  # наполняем параметрами запуска

driver = webdriver.Chrome(service=s, options=options)
driver.implicitly_wait(10)
driver.get('https://www.mvideo.ru')

button = driver.find_element(By.CLASS_NAME, 'tab-button')

button_trend = button[1]
button_trend.click()
trends = driver.find_element(By.XPATH, "//mvid-shelf-group[@class='page-carousel-padding ng-star-inserted']")


while True:
    try:
        button = driver.find_element(By.XPATH, '//span[contains(text(), "В тренде"]')
        button.click()
        break
    except:
        driver.find_element(By.CLASS_NAME, "popmechanic-deskpot").send_keys(Keys.PAGE_DOWN)

list_items = []
for item in trends:
    item_info = {}

    goods = button[0].find_elements(By.XPATH, "./ancestor::mvid-shelf-group")
    name = goods[0].find_elements(By.XPATH, "//div[@class='title']")
    link = goods[0].find_elements(By.XPATH, "//div[@class='title']/a[@href]")
    rating_list = goods[0].find_elements(By.XPATH, "//div[@class='product-mini-card__rating ng-star-inserted']//"
                                                   "span[@class='value ng-star-inserted']")
    price = goods[0].find_elements(By.XPATH, "//div[@class='product-mini-card__price ng-star-inserted']//"
                                             "span[@class='price__main-value']")

    item_info['name'] = name.text
    item_info['rating'] = rating_list.text
    item_info['link'] = link.get_attribute("href")
    item_info['price'] = price.text
    list_items.append(item_info)

    pprint(list_items)

db.base_mvideo.insertOne(list_items)

driver.close()

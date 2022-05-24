"""
Необходимо собрать информацию о вакансиях на вводимую должность (используем input) с сайтов Superjob(необязательно)
 и HH(обязательно). Приложение должно анализировать несколько страниц сайта (также вводим через input).
Получившийся список должен содержать в себе минимум:
1.	Наименование вакансии.
2.	Предлагаемую зарплату (разносим в три поля: минимальная и максимальная и валюта. цифры преобразуем к цифрам).
3.	Ссылку на саму вакансию.
4.	Сайт, откуда собрана вакансия.
По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение).
Структура должна быть одинаковая для вакансий с обоих сайтов.
Общий результат можно вывести с помощью dataFrame через pandas. Сохраните в json либо csv.
"""

import requests
import re
import pprint
from bs4 import BeautifulSoup as bs
import json

vacancy = input('введите название вакансии: ')
link = 'https://hh.ru/search/vacancy'

headers = {'user-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                         ' AppleWebKit/537.36 (KHTML, like Gecko)'
                         ' Chrome/101.0.4951.67 Safari/537.36'}
vacancy_database = []


def _parse_hh(vacancy):
    vacancy_date = []
    page = 0
    max_page = 39

    while page <= max_page:
        params = {
            'text': vacancy,
            'search_field': 'name',
            'page': page}
        html = requests.get(link, params=params, headers=headers)
        soup = bs(html.text, 'html.parser')
        vacancies = soup.find_all('div', {'class': 'vacancy-serp-item'})
        for i in vacancies:
            vacancy_info = {}

            # название вакансии
            vacancy_name = i.find('a', {'data-qa': 'vacancy-serp__vacancy-title'}).getText().replace(u'\xa0', u' ')
            vacancy_info['vacancy_name'] = vacancy_name

            # заработная плата
            salary = i.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
            if not salary:
                salary_min = None
                salary_max = None
                salary_currency = None
            else:
                salary = salary.getText() \
                    .replace(u'\xa0', u'')

                salary = re.split(r'\s|-', salary, 2)
                if salary[0] == 'до':
                    salary_min = None
                    salary_max = int(salary[1])
                elif salary[0] == 'от':
                    salary_min = int(salary[1])
                    salary_max = None
                else:
                    salary_min = int(salary[0])
                    salary_max = int(salary[1])
                salary_currency = salary[2]

            vacancy_info['salary_min'] = salary_min
            vacancy_info['salary_max'] = salary_max
            vacancy_info['salary_currency'] = salary_currency

            # ссылка на вакансию
            vacancy_link = i.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})['href']
            vacancy_info['vacancy_link'] = vacancy_link

            # сайт, с которого взята вакансия
            vacancy_info['site'] = 'hh.ru'

            vacancy_date.append(vacancy_info)
        page += 1

    return vacancy_date


vacancy_database.extend(_parse_hh(vacancy))

with open('data.json', 'w') as f:
    json.dump(vacancy_database.json(), f)

pprint(vacancy_database)

"""
1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию,
 которая будет добавлять только новые вакансии в вашу базу.
2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой
 больше введённой суммы (необходимо анализировать оба поля зарплаты).
Для тех, кто выполнил задание с Росконтролем - напишите запрос для поиска продуктов с рейтингом не ниже введенного
или качеством не ниже введенного (то есть цифра вводится одна, а запрос проверяет оба поля)

"""

import requests
import re
from pprint import pprint
from bs4 import BeautifulSoup as bs
import json

from pymongo import MongoClient


with open(vacancy_database.json') as f:
    vacancy_database_mongo = json.load(f)  # открываю сохраненную базу вакансий

client = MongoClient('127.0.0.1', 27017)  # подключаюсь к mongo
db = client['vacancy2022']  # присваиваю имя
vac = db.vacancy_database_mongo  # создаю коллекцию

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
            s = []
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
                elif salary[1] == "":
                    s = salary[2].split(' ', 2)
                    salary_min = int(salary[1])
                    salary_max = int(s[1])
                    salary[2] = s[2]
                else:
                    salary_min = int(salary[0])
                    salary_max = int(salary[1])
                salary_currency = salary[2]

            vacancy_info['salary_min'] = salary_min
            vacancy_info['salary_max'] = salary_max
            vacancy_info['salary_currency'] = salary_currency

            # ссылка на вакансию
            vacancy_link = i.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})['href']
            vacancy_info['vacancy_link'] = vacancy_link.split('?', 1)[0]  # формирую link до "?"

            # сайт, с которого взята вакансия
            vacancy_info['site'] = 'hh.ru'

            # вставляем новую вакансию в первоначальную базу данных после проверки до "?"
            if vacancy_info['vacancy_link'] != vac['vacancy_link']:  # проверяю вакансию на совпадение урлов
                vac.insert_one(vacancy_info)  # при отсутствии совпадений добавляю вакансию в базу

        page += 1

    return vac


vacancy_database.extend(_parse_hh(vacancy))


def find_salary():
    salary = input('Введите минимальную зарплату: ')
    for i in vac.find({'$or': [{'salary_min': {'$gte': salary}},
                               {'salary_max': {'$gte': salary}}]
                       }):
        pprint(i)


find_salary()

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import re

from itemadapter import ItemAdapter
from pymongo import MongoClient


class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.vacancy0606

    def process_item(self, item, spider):
        print()
        if spider.name == 'hhru':
            item['salary_min', 'salary_max', 'currency'] = self.process_salary(item['salary'])
        collection = self.mongobase[spider.name]
        collection.insert_one(item)
        return item

    def process_salary(self, salary):
        s = []
        if not salary:
            salary_min = None
            salary_max = None
            currency = None
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
                currency = salary[2]
            return salary_min, salary_max, currency

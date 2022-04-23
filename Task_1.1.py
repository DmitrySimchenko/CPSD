"""1.	Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев
 для конкретного пользователя, сохранить JSON-вывод в файле *.json;
  написать функцию, возвращающую(return) список репозиториев.
"""
# https://docs.github.com/en/rest/reference/repos#list-repositories-for-a-user

import requests
import json

username = 'DmitrySimchenko'  # мое имя на github
# input("Введите имя пользователя на github: ") - если необходимо вести
url = 'https://api.github.com'
# input("Введите адрес сайта: ") - введите адрес сайта
r = requests.get(f'{url}/users/{username}/repos')
# print(r.json()) - смотрим информацию о репозитории


# сохраняем в файле r.json
with open('data.json', 'w') as f:
    json.dump(r.json(), f)


# выводим список репозиториев
print(f'Репозитории {username}: ')
for i in r.json():
    print(i['name'])


""" Через функцию вывод почему-то не работает
def get_names(x):
    names = []
    for i in x:
        names.append(i['name'])
    return 'names'


print(f'Репозитории {username}: ', get_names(r))
"""
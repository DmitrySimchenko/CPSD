"""2.	Зарегистрироваться на https://openweathermap.org/api и написать функцию,
 которая получает погоду в данный момент для города, название которого получается через input.
  https://openweathermap.org/current
"""
# 0adda7fdf5eb900f94503b2945ec3343 token - получаю после регистрации на сайтеpip

# https://api.openweathermap.org/data/2.5/weather?q={city name}&appid={API key}

import requests
city_name = input('Введите название города: ')
city_id = 0
appid = "0adda7fdf5eb900f94503b2945ec3343"
try:
    res = requests.get("http://api.openweathermap.org/data/2.5/find",
                 params={'q': city_name, 'type': 'like', 'units': 'metric', 'APPID': appid})
    data = res.json()
    cities = ["{} ({})".format(d['name'], d['sys']['country'])
              for d in data['list']]
    print("город:", cities)
    city_id = data['list'][0]['id']
    print('city_id=', city_id)
except Exception as e:
    print("Exception (find):", e)
    pass

try:
    res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                 params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
    data = res.json()
    print("состояние:", data['weather'][0]['description'])
    print("температура (С):", data['main']['temp'])
    print("минимальная температура (С):", data['main']['temp_min'])
    print("максимальная температура (С):", data['main']['temp_max'])
except Exception as e:
    print("Exception (weather):", e)
    pass




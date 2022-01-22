import requests
from assistant import secrets
import os
import yaml

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Weather:
    base_url = 'https://api.openweathermap.org/data/2.5/'
    city_id = None
    appid = secrets.OPEN_WEATHER_MAP
    params = {'q': 'city', 'type': 'like', 'units': 'metric', 'APPID': appid }

    @classmethod
    def _get_cities(cls, city):
        params = cls.params.copy()
        params['q'] = city
        res = requests.get(
            cls.base_url + 'find',
            params=params,
        )
        data = res.json()
        if len(data['list']) > 0:
            return False, set([d['sys']['country'] for d in data['list']])
        cls._add_city_id(city, data['list'][0]['id'])
        return True,

    @classmethod
    def get_weather_now(cls, city):
        cls._init()
        params = cls.params.copy()
        params['q'] = city
        one_city_this_name = cls._get_cities(city)
        if one_city_this_name[0]:
            res = requests.get(
                cls.base_url + '/weather',
                params=params,
            )
            data = res.json()
            print(data)
            print("conditions:", data['weather'][0]['description'])
            print("temp:", data['main']['temp'])
            print("temp_min:", data['main']['temp_min'])
            print("temp_max:", data['main']['temp_max'])
        else:
            return one_city_this_name

    @classmethod
    def get_forecast(cls, city):
        cls._init()
        params = cls.params.copy()
        params['q'] = city
        one_city_this_name = cls._get_cities(city)
        if one_city_this_name[0]:
            res = requests.get(
                cls.base_url + '/weather',
                params=params,
            )
            data = res.json()

        else:
            print('error')

    @classmethod
    def _init(cls):
        if cls.city_id is None:
            with open(_BASE_DIR + '/helpers/weather.yaml', 'r') as file:
                cls.city_id = yaml.safe_load(file)
                if cls.city_id is None:
                    cls.city_id = {}

    @classmethod
    def _add_city_id(cls, city, id_):
        cls.city_id[city] = id_
        with open(_BASE_DIR + '/helpers/weather.yaml', 'w') as file:
            yaml.dump(cls.city_id, file)


Weather.get_weather_now('Северск')

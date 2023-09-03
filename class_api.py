import os
from abc import ABC, abstractmethod

import requests

api_key = os.getenv('API_SuperJob')
url_hh_ru = 'https://api.hh.ru/vacancies'
url_SuperJob = ''


class Api(ABC):
    @abstractmethod
    def get_vacancies(self):
        pass


class HeadHunterAPI(Api):

    def get_vacancies(self, name):
        params = {
            'per_page': 100,
            'text': name
        }
        res = requests.get(url=url_hh_ru, params=params)
        return res.json()


class SuperJobAPI(Api):
    def get_vacancies(self):
        headers = {
            "Authorization": f"Bearer {api_key}"
        }
        res = requests.get(url=url_hh_ru, headers= headers)
        return res.json()


class Vacancy:
    def __init__(self, name, url, salary, requirements, currency):
        self.name = str(name)
        self.url = str(url)
        if salary is None:
            self.salary = None
        else:
            self.salary = int(salary)
        self.requirements = str(requirements)
        self.currency = str(currency)

def comparisons_salary():
    pass










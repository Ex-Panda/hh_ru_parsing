import json
import os
from abc import ABC, abstractmethod

import requests

api_key = os.getenv('API_SuperJob')
url_hh_ru = 'https://api.hh.ru/vacancies'
url_SuperJob = ''


class Api(ABC):
    @abstractmethod
    def get_vacancies(self, name):
        pass


class HeadHunterAPI(Api):

    def get_vacancies(self, name):
        s = []
        params = {
            'per_page': 100,
            'text': name
        }
        res = requests.get(url=url_hh_ru, params=params).json()

        for i in res['items']:
            if i['salary'] is None:
                s.append([i['name'], i['alternate_url'], None, None, None, i['snippet']['requirement']])
            else:
                s.append([i['name'], i['alternate_url'], i['salary']['from'], i['salary']['to'], i['salary']['currency'],
                  i['snippet']['requirement']])
        return s


# class SuperJobAPI(Api):
#     def get_vacancies(self, name):
#         headers = {
#             "Authorization": f"Bearer {api_key}"
#         }
#         res = requests.get(url=url_hh_ru, headers=headers).json()
#         return res.json()


class Vacancy:
    def __init__(self, name:str, url:str, salary_from:int, salary_to:int, currency:str, requirements:str):
        self.name = name
        self.url = url

        if salary_from is None:
            self.salary_from = None
        else:
            self.salary_from = salary_from

        if salary_to is None:
            self.salary_to = None
        else:
            self.salary_to = salary_to

        self.requirements = requirements

        if currency is None:
            self.currency = None
        else:
            self.currency = currency


def comparisons_salary():
    pass


class Saver(ABC):
    @abstractmethod
    def add_vacancy(self, vacancy):
        pass

    @abstractmethod
    def get_vacancies_by_salary(self, salary:str):
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy):
        pass


class JSONSaver(Saver):
    def add_vacancy(self, vacancy):
        return json.dumps(vacancy, ensure_ascii=False)

    def get_vacancies_by_salary(self, salary: str):
        pass

    def delete_vacancy(self, vacancy):
        pass

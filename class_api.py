import json
import os
from abc import ABC, abstractmethod

import requests

api_key = os.getenv('API_SuperJob')
url_hh_ru = 'https://api.hh.ru/vacancies'
url_SuperJob = 'https://api.superjob.ru/2.0/vacancies/'


class Api(ABC):
    @abstractmethod
    def get_vacancies(self, name):
        pass


class HeadHunterAPI(Api):

    def get_vacancies(self, name):
        """Функция получает список вакансий с HeadHunter"""
        s = []
        params = {
            'per_page': 100,
            'text': name
        }
        res = requests.get(url=url_hh_ru, params=params).json()

        for i in res['items']:
            if i['salary'] is not None:
                s.append(
                    [i['name'], i['alternate_url'], i['salary']['from'], i['salary']['to'], i['salary']['currency'],
                     i['snippet']['requirement']])
        return s


class SuperJobAPI(Api):
    def get_vacancies(self, name):
        """Функция получает список вакансий с SuperJob"""
        s = []
        headers = {
            'X-Api-App-Id': api_key
        }
        params = {
            'keyword': name
        }
        res = requests.get(url=url_SuperJob, params=params, headers=headers).json()
        for i in res['objects']:
            s.append(
                [i['profession'], i['link'], i['payment_from'], i['payment_to'], i['currency'], i['candidat']])
        return s


class Vacancy:
    def __init__(self, name:str, url:str, salary_from:int, salary_to:int, currency:str, requirements:str):
        self.name = name
        self.url = url

        if salary_from is None and salary_to is not None:
            self.salary_from = salary_to
        else:
            self.salary_from = salary_from

        if salary_to is None and salary_from is not None:
            self.salary_to = salary_from
        else:
            self.salary_to = salary_to

        if salary_from is None and salary_to is None:
            self.salary_from = None
            self.salary_to = None

        self.requirements = requirements

        if currency is None:
            self.currency = ''
        else:
            self.currency = currency


def comparisons_salary(vacancy):
    """Функция сортировки вакансий по уменьшению заработной платы"""
    sorted_salary = sorted(vacancy, reverse=True, key=lambda x: x.salary_to)
    return sorted_salary


class Saver(ABC):
    @abstractmethod
    def add_vacancy(self, vacancy):
        pass

    @abstractmethod
    def get_vacancies_by_salary(self, salary:str):
        pass


class JSONSaver(Saver):
    def add_vacancy(self, vacancy):
        """Функция записи списка вакансий в файл"""
        file = open('vacancy_file.txt', 'w', encoding="utf-8")
        json.dump(vacancy, file, ensure_ascii=False)
        file.close()

    def get_vacancies_by_salary(self, salary: str):
        """Функция фильтрации по зарплатной вилке"""
        with open('vacancy_file.txt', 'r', encoding="utf-8") as file:
            file_json = json.load(file)
            salary_int = salary.split('-')
            list_vacancy = []
            for line in file_json:
                if line[2] is None and line[3] is None:
                    line[4] = ''
                elif line[2] is None and line[3] is not None:
                    line[2] = line[3]

                elif line[3] is None and line[2] is not None:
                    line[3] = line[2]

                elif int(salary_int[0]) >= line[2] and line[3] <= int(salary_int[1]):
                    list_vacancy.append(line)

        return list_vacancy


def print_vacancy(list_vacancy):
    """Фуекция вывода вакансий"""
    for vacancy in list_vacancy:
        print(f"""
название:{vacancy.name}
ссылка:{vacancy.url}
зарплата от:{vacancy.salary_from}
зарпалата до:{vacancy.salary_to}
валюта:{vacancy.currency}
требования:{vacancy.requirements}""")


def user_interaction():
    """Функция по работе с пользователем"""
    platforms = ["headhunter", "superjob"]
    query_platforms = input('С какой платформы хотите получить вакансии: HeadHunter или SuperJob? ').lower()

    if query_platforms not in platforms:
        print('С такой платформой не работаем')
    else:
        filter_words = input("Введите ключевое слово для поиска в названиях вакансий: ")
        if query_platforms == platforms[0]:
            api = HeadHunterAPI()
        else:
            api = SuperJobAPI()
        get_vacancies_filter_words = api.get_vacancies(filter_words)
        json_vacancy = JSONSaver()
        json_vacancy.add_vacancy(get_vacancies_filter_words)
        list_vacancy = []

        salary = input('Введите интересующую зарплатную вилку ')
        by_salary = json_vacancy.get_vacancies_by_salary(salary)
        for line in by_salary:
            vacancy = Vacancy(*line)
            list_vacancy.append(vacancy)
        sorted_vacancy = comparisons_salary(list_vacancy)
        if len(by_salary) == 0:
            print('Вакансий с указанной зарплатной вилкой не найдено')
        else:
            print_vacancy(sorted_vacancy)






from class_api import HeadHunterAPI

a = HeadHunterAPI()
b = a.get_vacancies('Python')
print(b)
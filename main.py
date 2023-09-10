from class_api import HeadHunterAPI, Vacancy, JSONSaver

a = HeadHunterAPI()
b = a.get_vacancies('Python')
c = JSONSaver()
n = c.add_vacancy(b)

print(b)
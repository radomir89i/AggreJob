import requests
from bs4 import BeautifulSoup
import json
import os
import csv


def csv_write(data,path):
    with open(path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for line in data:
            writer.writerow(line)


URL = 'https://api.hh.ru/vacancies'
HEADERS = {
    'User-Agent': 'api-test-agent'
}
PARAMS = {
    'text': 'Python',
    'page': 0,
    'per_page': '100',
    # 'pages': '2',
}
data = requests.get(URL, params=PARAMS, headers=HEADERS).json() # just to get page quantity

vacancies = set()

# now collect vacancy ids from all pages
for _ in range(data['pages']):
    new_data = requests.get(URL, params=PARAMS, headers=HEADERS).json()
    new_vacancies = {i['id'] for i in new_data['items']}
    vacancies = vacancies.union(new_vacancies)
    PARAMS['page'] += 1

# now we can inspect every vacancy
data = ['vacancy_id,vacancy_name,salary_from,salary_to,currency,area'.split(',')]
count = 30
for vacancy_id in vacancies:
    count -= 1
    if count < 1:
        break
    vacancy_data = requests.get(os.path.join(URL, vacancy_id)).json()
    name = vacancy_data.get('name')
    salary = vacancy_data.get('salary')
    if salary:
        salary_from = salary.get('from')
        salary_to = salary.get('to')
        currency = salary.get('currency')
    else:
        salary_from, salary_to, currency = None, None, None
    area = vacancy_data['area']['name']
    data.append([vacancy_id, name, salary_from, salary_to, currency, area])
    print([vacancy_id, name, salary_from, salary_to, currency, area])
csv_write(data, 'output.txt')

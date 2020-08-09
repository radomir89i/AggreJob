import requests
from bs4 import BeautifulSoup
import json
import os

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
for vacancy_id in vacancies:
    vacancy_data = requests.get(os.path.join(URL, vacancy_id)).json()
    print(vacancy_data.get('name'), vacancy_data.get('salary'), vacancy_data['area']['name'])
'''for vacancy in vacancies:
    try:
        print(vacancy.get('name') or 'No info',
              vacancy['salary']['from'] if vacancy['salary'] else 'No info',
              # vacancy.get('salary')['currency']
              # vacancy.get('key_skills'),
              # vacancy.get('has_test'),
              # vacancy.get('description')
              )
        req = requests.get(os.path.join(URL, vacancy['id']))

        if req.json().get('area'):
            area_name = req.json().get('area')['name']
            print(area_name)
        if req.json().get('key_skills'):
            key_skills = req.json().get('key_skills')
            for skill in key_skills:
                print(skill['name'], end=' ')
            print('\n')
        for key in vacancy:
            print(key, vacancy[key])
        if req.json().get('description'):
            soup = BeautifulSoup(req.json().get('description'))
            text = soup.get_text()
            print(req.json().get('description'))
    except TypeError:
        print(vacancy)'''

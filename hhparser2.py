import requests
import json
import os

URL = 'https://api.hh.ru/vacancies'
HEADERS = {
    'User-Agent': 'api-test-agent'
}
PARAMS = {
    'text': 'Python',
    # 'page': '55',
    'per_page': '100',
    # 'pages': '2',
}
r = requests.get(URL, params=PARAMS, headers=HEADERS)
data = r.json()
print('data received', data)
vacancies = data['items']
print(len(vacancies), ' vacancies found')
print(data['found'])
'''for vacancy in vacancies:
    try:
        print(vacancy['name'] or 'No info',
              vacancy['salary']['from'] if vacancy['salary'] else 'No info',
              vacancy.get('salary')['currency']
              # vacancy.get('key_skills'),
              # vacancy.get('has_test'),
              # vacancy.get('description')
              )
        req = requests.get(os.path.join(URL, vacancy['id']))
        key_skills = req.json().get('key_skills')
        area_name = req.json().get('area')['name']
        print(area_name)
        for skill in key_skills:
            print(skill['name'], end=' ')
        print('\n')
    except TypeError:
        print(vacancy)
'''
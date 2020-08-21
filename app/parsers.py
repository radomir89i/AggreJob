from abc import ABC, abstractmethod
import requests
import re


class Parser(ABC):
    @abstractmethod
    def __init__(self, main_skill, *key_skills):
        self.main_skill = main_skill
        self.key_skills = key_skills

    @abstractmethod
    def parse(self):
        pass

    @staticmethod
    def clean_vacancy_data(vacancy):
        vacancy_data = {
            'name': vacancy['name'],
            'area': vacancy['area']['name'],
        }

        if vacancy_data.get('salary'):
            vacancy_data['salary_from'] = vacancy['salary'].get('from')
            vacancy_data['salary_from'] = vacancy['salary'].get('from')
            vacancy_data['salary_currency'] = vacancy['salary']['currency']
            vacancy_data['salary_gross'] = vacancy['salary']['gross']

        vacancy_skill_set = set()

        words = re.split(r'[;,"\(\)\{\}/\s]', str(vacancy))
        words =[word.lower() for word in words]
        for skill in Parser.KEY_SKILLS:
            if skill in words:
                vacancy_skill_set.add(skill)
        vacancy_data['skill_set'] = vacancy_skill_set

        return vacancy_data

    @staticmethod
    def write_csv_file(path, data):
        pass

    KEY_SKILLS = {
        'python',
        'django',
        'git',
        'postgresql',
        'linux',
        'sql',
        'docker',
        'mysql',
        'rest',
        'r',
        'javascript',
        'html',
        'ms sql',
        'angularjs',
        'atlassian jira',
        'mongodb',
        'c++',
        'css',
        'nginx',
        'redis',
        'react',
        'pytorch',
        'flask',
        'bash',
        'php',
    }


class HHParser(Parser):
    def __init__(self, main_skill, *key_skills):
        Parser.__init__(self, main_skill, *key_skills)
        self.PARAMS = {
            'text': self.main_skill,
            'per_page': '100',
            'page': 0,
        }

    URL = 'https://api.hh.ru/vacancies'
    HEADERS = {
        'User-Agent': 'api-test-agent'
    }

    def parse(self):
        result = {}
        data = requests.get(self.URL, params=self.PARAMS, headers=self.HEADERS).json()
        current_page_vacancies = data['items']
        pages = data['pages']
        for i in range(1): # change to pages
            self.PARAMS['page'] = i
            print(self.PARAMS['page'])
            for vacancy in current_page_vacancies:
                vac_data = requests.get(self.URL + '/' + vacancy['id'], params=self.PARAMS).json()
                '''vac_id = vac_data['id']
                vac_name = vac_data['name']
                result[vac_id] = vac_name'''

                vac_id = vac_data['id']
                cleaned_data = Parser.clean_vacancy_data(vacancy)
                result[vac_id] = cleaned_data

        return result


class MKParser:
    def parse(self):
        pass


if __name__ == '__main__':
    parser = HHParser('python')
    print(parser.parse())

from abc import ABC, abstractmethod
import requests
import re
import yaml
import csv
from bs4 import BeautifulSoup
import lxml

CONFIG_PATH = 'config/spec_key_skills.yml'


class Parser(ABC):
    @staticmethod
    def _get_key_skills(specialization: str) -> list:
        """Get key skills from config.yml file"""
        with open(CONFIG_PATH) as f:
            config = yaml.safe_load(f)
        return config[specialization]

    @abstractmethod
    def parse(self) -> list:
        """Parses vacancy text """
        pass

    @abstractmethod
    def clean_vacancy_data(self, vacancy: dict) -> list:
        """Cleans vacancy text """
        pass

    @staticmethod
    def write_csv_file(path, data: list):
        """Writes parsing result to csv file"""
        with open(path, "w") as f:
            writer = csv.writer(f, delimiter=",")
            writer.writerows(data)


class HHParser(Parser):

    URL = 'https://api.hh.ru/vacancies'
    HEADERS = {
        'User-Agent': 'api-test-agent'
    }

    def __init__(self, specialization):
        self.specialization = specialization
        self.key_skills = Parser._get_key_skills(self.specialization)
        self.params = {
            'text': self.specialization,
            'per_page': '100',
            'page': 0,
        }

    def clean_vacancy_data(self, vacancy):
        vac_id = vacancy.get('id')
        name = vacancy.get('name')
        salary = vacancy.get('salary')
        if salary:
            salary_from = salary.get('from')
            salary_to = salary.get('to')
            currency = salary.get('currency')
        else:
            salary_from, salary_to, currency = None, None, None
        area = vacancy['area']['name']

        skill_set = []
        words = re.split(r'[;,"\(\)\{\}/\s]', str(vacancy))
        words = [word.lower() for word in words]
        for skill in self.key_skills:
            if skill in words:
                skill_set.append(skill)

        description = BeautifulSoup(vacancy.get('description'), 'lxml').text

        vacancy_data = [vac_id, name, salary_from, salary_to, currency, area, skill_set, description]

        return vacancy_data

    def parse(self):

        result = []
        result.append('id, name, salary_from, salary_to, currency, area, skill_set, description'.split(', '))
        s = requests.Session()
        pages = s.get(self.URL, params=self.params, headers=self.HEADERS).json()['pages']
        for i in range(pages):
            self.params['page'] = i
            data = s.get(self.URL, params=self.params, headers=self.HEADERS).json()
            current_page_vacancies = data['items']
            for vacancy in current_page_vacancies:
                vac_data = requests.get(self.URL + '/' + vacancy['id'], params=self.params).json()
                cleaned_data = HHParser.clean_vacancy_data(self, vac_data)
                result.append(cleaned_data)
        return result


class MKParser:
    def parse(self):
        pass


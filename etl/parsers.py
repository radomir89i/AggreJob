import re
from abc import ABC, abstractmethod

import requests
import yaml
import lxml
import csv
from bs4 import BeautifulSoup

from ..config import KEY_SKILLS_FILE


class Parser(ABC):
    @staticmethod
    def _get_key_skills(specialization: str) -> list:

        """
        Gets list of key skills for given specialization.
        Key skills are predetermined and are kept spec_key_skills.yml file.

        :param specialization: main programming language -> 'Python'
        :return: list of skills/technologies, connected to specialization -> ['django', 'git', 'linux']
        """

        with open(KEY_SKILLS_FILE) as f:
            config = yaml.safe_load(f)
        return config[specialization]

    @abstractmethod
    def parse(self) -> list:

        """
        Returns prepared data for writing in .csv file. The data is a list of lists(vacancies).
        The first list contains headers for .csv file -> ['vacancy_id, vacancy_name, url, source,
        salary_from, salary_to, currency, location, company, skill_set, description, publication_date']

        """
        pass

    @abstractmethod
    def clean_vacancy_data(self, vacancy: dict) -> list:

        """
        Parses vacancy data returned by source(job search website)
        :param vacancy: dict with vacancy data from source
        :return: list of needed vacancy info accordingly to .csv header
        """
        pass

    @staticmethod
    def write_csv_file(path, data: list) -> None:

        """
        Writes prepared data to adjusted .csv file.
        :param path: path to input file
        :param data: list of lists
        :return: None
        """

        with open(path, "w", encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=",")
            writer.writerows(data)


class HHParser(Parser):

    URL = 'https://api.hh.ru/vacancies'
    HEADERS = {
        'User-Agent': 'api-test-agent'
    }

    def __init__(self, specialization: str):
        self.specialization = specialization
        self.key_skills = Parser._get_key_skills(self.specialization)
        self.params = {
            'text': self.specialization,
            'per_page': '100',
            'page': 0,
        }

    def clean_vacancy_data(self, vacancy):
        vacancy_id = vacancy.get('id')
        vacancy_name = vacancy.get('name')
        url = vacancy.get('alternate_url')
        source = 'HH'
        salary = vacancy.get('salary')
        employer = vacancy['employer']['name']
        publication_date = vacancy.get('published_at').split('T')[0]

        if salary:
            salary_from = salary.get('from')
            salary_to = salary.get('to')
            currency = salary.get('currency')
        else:
            salary_from, salary_to, currency = None, None, None
        location = vacancy['area']['name']

        skill_set = []
        words = re.split(r'[;,"\(\)\{\}/\s]', str(vacancy))
        words = [word.lower() for word in words]

        for skill in self.key_skills:
            if skill in words:
                skill_set.append(skill)

        description = BeautifulSoup(vacancy.get('description'), 'lxml').text

        vacancy_data = [vacancy_id, vacancy_name, url, source, salary_from,
                        salary_to, currency, location, employer,
                        skill_set, description, publication_date]

        return vacancy_data

    def parse(self):

        result = []
        result.append('vacancy_id, vacancy_name, url, source, '
                      'salary_from, salary_to, currency, location, '
                      'company, skill_set, description, publication_date'.split(', '))

        s = requests.Session()

        pages = s.get(self.URL, params=self.params, headers=self.HEADERS).json()['pages']
        for i in range(1):  # replace with 'pages' variable
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


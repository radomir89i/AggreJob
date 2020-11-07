import re
import os
import csv
import logging
from abc import ABC, abstractmethod

import requests
import yaml
import lxml
from bs4 import BeautifulSoup

from config import Config


def catching_errors(func):
    def wrapped(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            logging.error(f'{e}')

    return wrapped


class Parser(ABC):
    @staticmethod
    def _get_key_skills(specialization: str) -> list:

        """
        Gets list of key skills for given specialization.
        Key skills are predetermined and are kept spec_key_skills.yml file.

        :param specialization: main programming language -> 'Python'
        :return: list of skills/technologies, connected to specialization -> ['django', 'git', 'linux']
        """

        with open(Config.KEY_SKILLS_FILE) as f:
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
    @catching_errors
    def write_csv_file(path, data: list) -> None:

        """
        Writes prepared data to adjusted .csv file.
        :param path: path to input file
        :param data: list of lists
        :return: None
        """

        logging.info(f'creating file {path} ...')
        with open(path, "w", encoding='utf-8', newline='\n') as f:
            writer = csv.writer(f, delimiter=",")
            logging.info('writing rows to file ...')
            writer.writerows(data)
            logging.info('writing finished')
        logging.info('file closed')


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

    @catching_errors
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

        is_actual = True

        vacancy_data = [vacancy_id, vacancy_name, url, source, employer,
                        salary_from, salary_to, currency, location,
                        skill_set, description, is_actual, publication_date]

        return vacancy_data

    @catching_errors
    def parse(self):

        result = []
        result.append('vacancy_id, vacancy_name, url, source, '
                      'company, salary_from, salary_to, currency, location, '
                      ' skill_set, description, is_actual, publication_date'.split(', '))

        s = requests.Session()

        logging.info('start of parsing ...')
        pages = s.get(self.URL, params=self.params, headers=self.HEADERS).json()['pages']

        for i in range(1):
            logging.info(f'parsing vacancies from page {i} of {pages} ...')
            self.params['page'] = i
            logging.info('requesting IDs of current page vacancies ...')
            data = s.get(self.URL, params=self.params, headers=self.HEADERS).json()
            current_page_vacancies = data['items']

            logging.info('requesting and parsing data for vacancies ...')
            for vacancy in current_page_vacancies:
                vac_data = requests.get(self.URL + '/' + vacancy['id'], params=self.params).json()
                cleaned_data = HHParser.clean_vacancy_data(self, vac_data)
                result.append(cleaned_data)

        logging.info('parsing finished')
        return result






from abc import ABC, abstractmethod
import requests
import re
import yaml
import csv
from bs4 import BeautifulSoup
import lxml

CONFIG_PATH = '../config/spec_key_skills.yml'


# def get_ll_by_address(address='Андропова пр-т, 18 к.9, Москва'):
#     """Эта функция возвращает координаты по адресу или сообщение об ошибке
#
#     :param address: адрес объекта, следующего формата -> "Андропова пр-т, 18 к.9, Москва"
#     :type  address: str
#
#     :rtype: dict
#     :return: в случае успешного декодирования -> {"status": "ok", "ll": (lon, lat)}
#              в случае ошибки при запросе      -> {"status": "error", "msg": "some_error_msg"}
#     """
#     addr = '%20'.join(address.split(' '))
#     ll_content = {'status': 'ok', 'll':()}
#     params = f'q={addr}&format=json'
#     url = f'http://search.maps.sputnik.ru/search/addr?{params}'
#     try:
#         # data = req.get(url).json()['result'].get('address')
#         data = req.get(url, proxies={'http': 'http://bproxy.msk.mts.ru:3128'}).json()['result'].get('address')
#
#         if data is not None:
#             ll = data[0]['features'][0]['geometry']['geometries'][0]['coordinates']
#             ll_content['ll'] = ll
#         else:
#             ll_content['status'] =  'error'
#             ll_content['msg'] = f'Not found coordinates by addr="{address}"'
#     except Exception as e:
#         ll_content = {'status': 'error', 'msg': str(e)}
#
#     return ll_content

class Parser(ABC):
    @staticmethod
    def _get_key_skills(specialization: str) -> list:
        """
        Load key_skills for each specialization from yaml config

        :param specialization:
        :return:
        """
        """"""
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
        employer = vacancy['employer']['name']
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

        vacancy_data = [vac_id, name, salary_from, salary_to, currency, area, employer, skill_set, description]

        return vacancy_data

    def parse(self):

        result = []
        result.append('id, name, salary_from, salary_to, currency, area, employer, skill_set, description'.split(', '))
        s = requests.Session()
        pages = s.get(self.URL, params=self.params, headers=self.HEADERS).json()['pages']
        for i in range(1):
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


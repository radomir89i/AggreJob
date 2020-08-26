from abc import ABC, abstractmethod
import requests
import re
import yaml


class Parser(ABC):
    @staticmethod
    def get_config(parameter):
        """Get parameter from config.yml file"""

        with open('config.yml') as f:
            config = yaml.safe_load(f)
        return config[parameter]

    @abstractmethod
    def __init__(self, specialization):
        self.specialization = specialization

    @abstractmethod
    def parse(self):
        pass

    @abstractmethod
    def clean_vacancy_data(self, vacancy):
        pass

    @staticmethod
    def write_csv_file(path, data):
        pass


class HHParser(Parser):
    def __init__(self, specialization):
        Parser.__init__(self, specialization)
        self.KEY_SKILLS = Parser.get_config('KEY_SKILLS')
        self.params = {
            'text': self.specialization,
            'per_page': '100',
            'page': 0,
        }

    URL = 'https://api.hh.ru/vacancies'
    HEADERS = {
        'User-Agent': 'api-test-agent'
    }

    def clean_vacancy_data(self, vacancy):
        """Cleans vacancy text """

        vacancy_data = {
            'name': vacancy['name'],
            'area': vacancy['area']['name'],
        }

        if vacancy_data.get('salary'):
            vacancy_data['salary_from'] = vacancy['salary'].get('from')
            vacancy_data['salary_from'] = vacancy['s alary'].get('from')
            vacancy_data['salary_currency'] = vacancy['salary']['currency']
            vacancy_data['salary_gross'] = vacancy['salary']['gross']

        vacancy_skill_set = set()

        words = re.split(r'[;,"\(\)\{\}/\s]', str(vacancy))
        words =[word.lower() for word in words]
        for skill in self.KEY_SKILLS:
            if skill in words:
                vacancy_skill_set.add(skill)
        vacancy_data['skill_set'] = vacancy_skill_set

        return vacancy_data

    def parse(self):
        """Parses vacancy text """
        result = {}
        data = requests.get(self.URL, params=self.params, headers=self.HEADERS).json()
        current_page_vacancies = data['items']
        pages = data['pages']
        for i in range(1): # change range(x) to 'pages' to go for a full cycle
            self.params['page'] = i
            print(i)
            for vacancy in current_page_vacancies:
                vac_data = requests.get(self.URL + '/' + vacancy['id'], params=self.params).json()
                '''vac_id = vac_data['id']
                vac_name = vac_data['name']
                result[vac_id] = vac_name'''

                vac_id = vac_data['id']
                # print(vac_id)
                cleaned_data = HHParser.clean_vacancy_data(self, vacancy)
                # print(cleaned_data)
                result[vac_id] = cleaned_data

        return result


class MKParser:
    def parse(self):
        pass


if __name__ == '__main__':
    parser = HHParser('python')
    print(parser.parse())

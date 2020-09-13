from abc import ABC, abstractmethod
import requests
import re
import yaml
import csv
from bs4 import BeautifulSoup
import lxml


class Parser(ABC):
    @staticmethod
    def _get_key_skills(path, specialization: str) -> list:
        """Get key skills from config.yml file"""
        with open(path) as f:
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



if __name__ == "__main__":
    s = '39048643,Java / C / C++ Software Developer,130000,,RUR,Новосибирск,"['spring', 'sql', 'hibernate', 'docker', 'c++']","Удаленная работа. Полный рабочий день. Что делаем Разрабатываем серверные продукты для стриминга. Наша платформа используется другими разработчиками по всему миру в качестве бэкенда для приложений потокового видео, таких как онлайн-трансляции, конференции, видеочаты, вебинары, видеозвонки, видеонаблюдение, и т. д. Например, если разработчик работает над веб-проектом, он может взять HTTP сервер (сервлет контейнер) Tomcat или Spring Boot + Embed Tomcat. Если же проект требует работы с видео реального времени, трансляциями и передачей видеоданных, разработчик использует наш сервер приложений WCS. Т.е. Мы разрабатываем сервер приложений, который занимается видео, принимает и распределяет видеопотоки, конвертирует в различные протоколы и раздает на мобильные и веб-приложения. Кого ищем Ищем достаточно низкоуровневого программиста Java / C. Низкоуровневость заключается в том, что придется напрямую работать с сетевыми протоколами, байтами, буферами, многопоточностью, реалтаймом, Java SE, и писать код, устойчивый к большим нагрузкам. Сервер может пропускать гигабиты видео в секунду. Это действительно большие нагрузки, которые внутри обрабатываются большим количеством тредов. Отсюда многопоточность. Критичные вычислительные задачи, связанные с обработкой сигналов вынесены в C часть через JNI. Поэтому в какой-то части кода вероятно придется работать с C или C++. Вам скорее всего не понравится работать над задачами проекта, если вы больше предпочитаете или привыкли работать с текущими высокоуровневыми веб-стеками и фреймворками, такими как Spring, Hibernate, SQL and NoSQL, и т. д. Кроме этого, у нас много легаси кода, который также нуждается в планомерном рефакторинге и улучшении. Если вы предпочитаете не работать с легаси кодом ни при каких условиях, эта вакансия вряд ли то, что вам нужно. Вам может подойти эта вакансия если есть опыт и желание развиваться в этом направлении, решать схожие низкоуровневые задачи, работать с сетевыми протоколами из Java напрямую, разбираться как устроен транспорт аудио и видеопотоков по сети, изучать спецификации и драфты, создавать надежный код, устойчивый к нагрузкам и выполнению в многопоточной среде, рефакторить и улучшать существующую кодовую базу. Требования  Java SE C/C++ желательно Linux на уровне продвинутого пользователя или администратора Опыт работы с сетевыми протоколами, клиент-сервер, TCP IP, UDP, возможно другими низкоуровневыми вещами на Java или C / C++  Условия  Удаленная работа. Полный рабочий день. ЗП от 130 т. р.  Ключевые слова, протоколы и технологии с которыми работаем WebRTC, RTMP, RTSP, HLS, RTCP, RTP, SRTP, SDP, SIP, ICE, STUN, DTLS, TCP, UDP, Websocket, TURN, MP4, webM, HTML5; H.264, VP8, VP9, Opus, AAC, Speex, G.711, G.729; Streaming, Calls, Transcoding, Encoder, Decoder, Mixing, Recording, Resampling, Player, Live encoder, CDN, MCU, SFU, VOD; Android, iOS, Linux, Docker, AWS, Camera, Microphone, IP cam, SIP PBX"

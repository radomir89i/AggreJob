import os
import csv
import logging

import psycopg2 as pg

from config import Config


def transaction_check(func):
    def wrapped(obj):
        try:
            func(obj)
        except Exception as e:
            logging.error(f'{e} - rolling back')
            obj._conn.rollback()
        finally:
            obj._conn.close()

    return wrapped


class Loader:
    def __init__(self, db_creds=Config.PG_CONNECTION, file_path=None, loading_type='INSERT'):
        """
        Класс Loader реализует логику загрузчика csv в БД

        :param creds: pg кредсы для psycopg2.connect
        :param file_path: путь до csv
        :param loading_type: принимает одно из след значений: 1. "INSERT" - импорт CSV в базу,
                                                              2. "UPDATE" - обновление уже имеющихся вакансий
        """

        self.loading_type = loading_type
        self.file_path = file_path
        logging.info('connecting to database ...')
        self._conn = pg.connect(db_creds)
        logging.info('connected to database')
        self._cur = self._conn.cursor()

    def vac_id_exists(self, vac_id: str) -> bool:
        """
        Checks if there is a vacancy with target id in database.
        """

        self._cur.execute("SELECT EXISTS(SELECT 1 FROM vacancy WHERE vacancy_id = %s)", (vac_id,))
        return self._cur.fetchone()[0]

    @transaction_check
    def from_csv_to_db(self) -> None:
        """
        Loads vacancies data from *.csv file into database.
        """

        logging.info(f'opening file {self.file_path} ...')
        with open(self.file_path, 'r', encoding='utf-8') as f:
            csv_reader = csv.reader(f, delimiter=',')
            next(csv_reader)

            logging.info('inserting rows into database ...')
            query = '''INSERT INTO vacancy (vacancy_id, vacancy_name, url, source, company,
                                            salary_from, salary_to, currency, location,
                                            skill_set, description, is_actual, publication_date)
                       VALUES  (%s, %s, %s, %s, %s, NULLIF(%s, '')::int, NULLIF(%s, '')::int, %s, %s, %s, %s, %s, %s)'''

            for row in csv_reader:
                if not self.vac_id_exists(row[0]):
                    self._cur.execute(query, tuple(row))

            self._conn.commit()
            logging.info('inserting finished')

    @transaction_check
    def _update_vacancy_status(self):
        pass

    def run(self):
        if self.loading_type == 'INSERT':
            self.from_csv_to_db()
        else:
            self._update_vacancy_status()


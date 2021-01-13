import csv
import logging

import psycopg2 as pg

from config import Config
from .parser import Parser


def transaction_check(func):
    """
    Decorator for closing db connection in case of errors
    """
    def wrapped(obj, *args, **kwargs):
        try:
            func(obj, *args, **kwargs)
        except Exception as e:
            logging.error(f'{e} - rolling back')
            obj._conn.rollback()
        finally:
            obj._conn.close()

    return wrapped


class Loader:
    def __init__(self, db_creds=Config.PG_CONNECTION, file_path=None, loading_type='INSERT'):
        """
        Class for loading vacancies from csv into database and updating statuses of vacancies.

        :param db_creds: credentials for connection to database using psycopg2
        :param file_path: *.csv file for loading into database
        :param loading_type: takes on of values: 1. "INSERT" - loading vacancies from csv into db,
                                                 2. "UPDATE" - updating 'is_actual' column for vacancies in db
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
            query_ins = '''INSERT INTO vacancy (vacancy_id, vacancy_name, url, source, company,
                                            salary_from, salary_to, currency, location,
                                            skill_set, description, is_actual, publication_date, specialization)
                       VALUES  (%s, %s, %s, %s, %s, NULLIF(%s, '')::int, NULLIF(%s, '')::int, %s, %s, %s, %s, %s, %s, %s)'''
            query_ups = '''UPDATE vacancy  
                           SET vacancy_name = %s, 
                              url = %s, 
                              source = %s, 
                              company = %s,
                              salary_from = NULLIF(%s, '')::int,
                              salary_to = NULLIF(%s, '')::int, 
                              currency = %s, 
                              location = %s,
                              skill_set = %s, 
                              description = %s, 
                              is_actual = %s, 
                              publication_date = %s, 
                              specialization = %s
                          WHERE vacancy_id = %s;'''

            for row in csv_reader:
                row[9] = row[9].split(',')[:-1]
                if not self.vac_id_exists(row[0]):
                    self._cur.execute(query_ins, tuple(row))
                else:

                    self._cur.execute(query_ups, tuple(row[1:]) + (row[0],))

            self._conn.commit()
            logging.info('inserting finished')

    @transaction_check
    def _update_vacancy_status(self) -> None:
        """
        Updates relevancy of all vacancies from database
        """
        for parser_class in Parser.__subclasses__():

            logging.info('querying vacancies for')
            query = 'SELECT vacancy_id from vacancy WHERE source = %s'
            self._cur.execute(query, (parser_class.SOURCE_NAME,))
            fetches = self._cur.fetchall()
            vacancies_from_db = [i[0] for i in fetches]
            logging.info(f'Got vacancies ids from database')

            logging.info('Requesting web source for irrelevant vacancies...')
            irrelevant_vacancies = parser_class('python').is_actual(vacancies_from_db)
            logging.info('Got irrelevant vacancies')

            logging.info('Updating "is_actual" status for irrelevant vacancies in database')
            query = 'UPDATE vacancy SET is_actual = %s WHERE source = %s and vacancy_id = %s'
            for vac_id in irrelevant_vacancies:
                self._cur.execute(query, ('FALSE', parser_class.SOURCE_NAME, vac_id))
            self._conn.commit()
            logging.info('Updating finished')

    def run(self):
        if self.loading_type == 'INSERT':
            self.from_csv_to_db()
        elif self.loading_type == 'UPDATE':
            self._update_vacancy_status()


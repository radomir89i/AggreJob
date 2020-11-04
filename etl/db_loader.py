import os
import csv
import logging

import psycopg2 as pg

from config import Config


def try_except_finally(func):
    def wrapped(obj):
        try:
            func(obj)
        except Exception as e:
            print(e)
            logging.error(f'{e} - rolling back')
            obj._conn.rollback()
        finally:
            obj._conn.close()

    return wrapped


class Loader:
    def __init__(self, db_creds=Config.PG_CONNECTION, file_path=None, loading_type='IMPORT'):
        """
        Класс Loader реализует логику загрузчика csv в БД

        :param creds: pg кредсы для psycopg2.connect
        :param file_path: путь до csv
        :param loading_type: принимает одно из след значений: 1. "IMPORT" - импорт CSV в базу,
                                                              2. "UPDATE" - обновление уже имеющихся вакансий
        """

        # todo: как делать соединение? Через пулл ресурсов или инициализировать в каждом Loader object?
        logging.info('connecting to database')
        self._conn = pg.connect(db_creds)
        logging.info('connected to database')
        self._cur = self._conn.cursor()
        self.loader_type = loading_type
        self.file_path = file_path

    def vac_id_exists(self, vac_id):
        self._cur.execute("SELECT EXISTS(SELECT 1 FROM vacancy WHERE vacancy_id = %s)", (vac_id,))
        return self._cur.fetchone()[0]

    # todo: добавить декоратор, который делает try, except, finally
    @try_except_finally
    def _import_csv_into_db(self):
        logging.info(f'opening file {self.file_path}')
        with open(self.file_path, 'r', encoding='utf-8') as f:
            csv_reader = csv.reader(f, delimiter=',')
            logging.info('reading csv file')
            next(csv_reader)
            logging.info('inserting rows into database')
            for row in csv_reader:
                if self.vac_id_exists(row[0]):
                    continue
                idx = row[0]
                name = row[1]
                url = row[2]
                source = row[3]
                salary_from = row[4] if row[4] else 0
                salary_to = row[5] if row[5] else 0
                currency = row[6]
                location = row[7]
                company = row[8]
                skill_set = row[9]
                description = row[10]
                is_actual = True
                publication_date = row[11]

                self._cur.execute(
                    'INSERT INTO vacancy VALUES (default, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                    [idx, name, url, source, company, salary_from,
                     salary_to, currency, location, skill_set,
                     description, is_actual, publication_date])
            self._conn.commit()
            logging.info('import finished')

    @try_except_finally
    def _update_vacancy_status(self):
        pass

    def run(self):
        if self.loader_type == 'IMPORT':
            self._import_csv_into_db()
        else:
            self._update_vacancy_status()


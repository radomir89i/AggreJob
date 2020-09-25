

class Loader:
    @staticmethod
    def load_data_from_csv_to_database():
        '''
        У нас будет два режима загрузка
            1. Просто добавляются данные, у которых publication_date >= last_publication_date
                + При таком сценарии мы получаем из БД последнюю publication_date для того спека, который собираемся парсить
                + Загружаем данные из источника (например hh)  по этому спеку, у которых publication_date >= last_publication_date в CSV
                + Удаляем записи с данным publication_date
                + Загружаем новые данные

            2. Пока не надо
        '''

        pass

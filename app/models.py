from app import db


class Vacancy(db.Model):
    # todo: add constraints to columns that should not equal to None
    # todo: add column publication date
    # todo: is_actual (bool -> True or False)
    __table_name__ = 'vacancies'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vacancy_id = db.Column(db.Integer, index=True, unique=True)
    vacancy_name = db.Column(db.String(64))
    source = db.Column(db.String(64))
    company = db.Column(db.String(64))
    salary_from = db.Column(db.Integer)
    salary_to = db.Column(db.Integer)
    currency = db.Column(db.String(16))
    location = db.Column(db.String(64))
    skill_set = db.Column(db.String(256))
    description = db.Column(db.Text)

    def __repr__(self):
        return '<Vacancy {}>'.format(self.vacancy_name)


class User(db.Model):
    __table_name__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

from app import db


class Vacancy(db.Model):
    __table_name__ = 'vacancies'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    vacancy_id = db.Column(db.String(64), index=True, unique=True)
    vacancy_name = db.Column(db.String(128), nullable=False)
    url = db.Column(db.String(64), nullable=False)
    source = db.Column(db.String(64), nullable=False)
    company = db.Column(db.String(128), nullable=False)
    salary_from = db.Column(db.Integer, nullable=True)
    salary_to = db.Column(db.Integer, nullable=True)
    currency = db.Column(db.String(16))
    location = db.Column(db.String(64), nullable=False)
    skill_set = db.Column(db.ARRAY(db.String))
    description = db.Column(db.Text)
    is_actual = db.Column(db.Boolean, default=True)
    publication_date = db.Column(db.Date, nullable=False)
    specialization = db.Column(db.String(16))

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

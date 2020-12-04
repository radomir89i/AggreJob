from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db, compare_type=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:dsr3629p@localhost:5432/vacancies_db'

from app import routes, models

# print(models.Vacancy.query.all())

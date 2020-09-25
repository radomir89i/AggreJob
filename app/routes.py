from flask import request
import pandas as pd
from app import app
import os

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/get_data')
def get_data():
    vacancy_name = request.args.get('vacancy_name')
    if vacancy_name == 'python':
        content = ''
        data = pd.read_csv('proper_data.csv', delimiter=',').values
        for row in data:
            content += str(list(row)) + '<br>'
        return content

    elif vacancy_name is not None and vacancy_name != 'python':
        return f'Has no data for vacancy_name={vacancy_name}'
    else:
        return 'Got no "vacancy_name" parameter'
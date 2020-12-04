import pandas as pd
import psycopg2 as pg

from flask import render_template, request, flash, redirect, url_for, jsonify

from app import app
from app.forms import LoginForm, JobSearchForm
from .models import Vacancy
from config import Config
from etl.parsers import Parser
from .utils import relevant_vacancies


@app.route('/')
def index():
    return render_template('base.html')


@app.route('/job_search')
def job_search():
    spec_list = ['Python', 'Java']
    return render_template('job_search.html', spec_list=spec_list)


@app.route('/win')
def win(formdata):
    render_template('formdata.html', formdata=formdata)


@app.route('/job_search_wtf', methods=['post', 'get'])
def job_search_wtf():
    skills = ['git', 'linux', 'django', 'postgresql']
    form = JobSearchForm()
    if form.validate_on_submit():
        specialization = form.specialization.data.lower()
        vacancies = relevant_vacancies(specialization, skills)
        print(vacancies[:5])
        return render_template('search_results.html', user_specialization=specialization, vacancies=vacancies)
    else:
        print(form.errors)
    return render_template('job_search_wtf.html', form=form)


@app.route('/skill/<specialization>')
def skill(specialization):
    skills = Parser._get_key_skills(specialization)
    return jsonify({'skills': skills})


@app.route('/find_vacancy')
def find_vacancy():
    form = SimpleForm()


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


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
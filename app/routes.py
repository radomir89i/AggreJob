from flask import render_template, request, flash, redirect, url_for, jsonify

from app import app
from app.forms import LoginForm, JobSearchForm
from .utils import relevant_vacancies


@app.route('/')
def index():
    return render_template('base.html')


@app.route('/results')
def results():
    specialization = request.args.get('specialization').lower()
    skills = request.args.get('skills_str').split()
    vacancies = relevant_vacancies(specialization, skills)
    return render_template('test_search_results.html', vacancies=vacancies)


@app.route('/find_job', methods=['post', 'get'])
def find_job():

    form = JobSearchForm()
    if form.validate_on_submit():
        skills = request.form.get('skills_str').split()
        specialization = form.specialization.data.lower()
        vacancies = relevant_vacancies(specialization, skills)
        checkbox = request.form.getlist('mycheckbox')
        return render_template('search_results.html', user_specialization=specialization, vacancies=vacancies)

    return render_template('find_job.html', form=form)


@app.route('/login', methods=['post', 'get'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)




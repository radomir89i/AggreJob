from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, SelectField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class JobSearchForm(FlaskForm):
    spec_list = ['Python', 'Java']
    choices = [(i, i) for i in spec_list]
    specialization = RadioField('Label', choices=choices, validators=[DataRequired()])  # choices=[('value', 'description'), ('value_two', 'whatever')])


'''class SimpleForm(FlaskForm):
    def __init__(self, specialization, skills):
        self.specialization = specialization
        self.skills = skills

    specialization = SelectField('specialization', choices=)'''
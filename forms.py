#!/usr/bin/python
# -*- coding: utf-8 -*-
from wtforms import Form, BooleanField, StringField, PasswordField, SelectField, FileField, SubmitField, validators


class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25),validators.DataRequired()])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('password_confirm', message='Passwords must match')
    ])
    password_confirm = PasswordField('Confirm Password',[validators.DataRequired()])
    email = StringField('Email Address', [validators.Length(min=6, max=35),validators.DataRequired()])
    accept_rules = BooleanField('I accept the site rules', [validators.InputRequired()])
    submit = SubmitField('Submit')


class FpsForm(Form):
    #code = StringField('Submission Code', [validators.InputRequired()])
    cpu = StringField('CPU', [validators.InputRequired()])
    gpu = StringField('GPU', [validators.InputRequired()])
    ram = StringField('RAM', [validators.InputRequired()])
#    resolution = SelectField('Reslution', choices=[ ('921600', '1280x720'),('1764000', '1680x1050'),('2073600', '1920x1080'), ('3686400', '2560x1440'), ('3686400', '2560x1440'), ('8294400', '3840x2160')], validators=[validators.InputRequired()])
    resolution = SelectField('Reslution', choices=[ ('1280x720', '1280x720'),('1680x1050', '1680x1050'),('1920x1080', '1920x1080'), ('2560x1440', '2560x1440'), ('2560x1440', '2560x1440'), ('3840x2160', '3840x2160')], validators=[validators.InputRequired()])
    sq_ver = SelectField('Squad Version', choices=[('0914', '9.14'), ('0915', '9.15'), ('0916', '9.16')], validators=[validators.InputRequired()])
    fps_values = FileField('FPS Values CSV file')
#    fps_values = FileField('FPS Values CSV file', [validators.regexp(ur'^[^/\\]\.csv$')])

class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password')
    submit = SubmitField('Submit')

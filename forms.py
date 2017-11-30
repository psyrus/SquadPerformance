#!/usr/bin/python
# -*- coding: utf-8 -*-
from wtforms import Form, BooleanField, StringField, FileField, validators


class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    accept_rules = BooleanField('I accept the site rules', [validators.InputRequired()])


class FpsForm(Form):
    cpu = StringField('CPU', [validators.InputRequired()])
    gpu = StringField('GPU', [validators.InputRequired()])
    ram = StringField('RAM', [validators.InputRequired()])
    #fps_values = FileField('FPS Values CSV file', [validators.regexp(u'^[^/\\]\.csv$')])
    fps_values = FileField('FPS Values CSV file')

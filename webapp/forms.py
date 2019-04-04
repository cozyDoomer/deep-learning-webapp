import re, os

from flask import current_app

from wtforms import Form, validators, StringField, TextAreaField, FileField



class EmailForm(Form):
    name = StringField(label=None, validators=[validators.DataRequired(), validators.Length(min=4, max=25)])
    email_field = StringField(label=None, validators=[validators.DataRequired(), validators.Email(), validators.Length(min=6, max=35)])
    message = TextAreaField(label=None, validators=[validators.DataRequired(), validators.Length(min=4, max=1000)])
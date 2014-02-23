from flask.ext.wtf import Form
from flask.ext.wtf.html5 import EmailField
from flask.ext.wtf.file import FileField, FileRequired, FileAllowed
from wtforms import validators, ValidationError, TextField, TextAreaField, SubmitField, PasswordField, SelectMultipleField, FormField, SelectField
from flask import session
from models import Member, db


class EventForm(Form):
	url = TextField('Event URL', [validators.Required()])

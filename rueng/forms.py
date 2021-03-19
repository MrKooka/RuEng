from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,BooleanField,PasswordField,IntegerField
from wtforms import TextAreaField,SelectField,SelectMultipleField,FormField
from wtforms.validators import InputRequired,Email,Length,DataRequired
from wtforms.fields.html5 import SearchField
import sys
import phonenumbers

class RegisterForm_(FlaskForm):
    email = StringField('Email:',validators=[Email('некорректный email')])
    telegramid = IntegerField('Ваш Telegram id')
    username = StringField('Ваше имя', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Пароль',validators=[InputRequired(), Length(min=8, max=80)])
    submit = SubmitField('Зарегистрироваться')
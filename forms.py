from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,BooleanField,PasswordField,IntegerField
from wtforms import TextAreaField,SelectField,SelectMultipleField,FormField
from wtforms.validators import InputRequired,Email,Length,DataRequired
from wtforms.fields.html5 import SearchField
import sys
from wtforms.widgets import TextArea


class RegisterForm_(FlaskForm):
    email = StringField('Email:',validators=[Email('некорректный email')])
    telegramid = StringField('Ваш Telegram id')
    username = StringField('Ваше имя', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Пароль',validators=[InputRequired(), Length(min=8, max=80)])
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(),Email()])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')
    submit = SubmitField('Войти')

class Add_word(FlaskForm):
	ru = StringField('Русский перевод',validators=[InputRequired()])
	eng = StringField('Английский перевод',validators=[InputRequired()])
	context = StringField('Контекст (максимальный размер - 225 символов)',widget=TextArea(),validators=[Length(min=0,max=225)])
	submit = SubmitField('Добавить')

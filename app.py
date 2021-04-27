from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from random import choice
from pprint import pprint
from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager
from flask_login import LoginManager
class Configurations:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:1@localhost:27017/rueng'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    SECRET_KEY = 'sdfewr4t56yuikhjmngfbdrew'

class SaveSelf:
	def __get__(self,instance, owner):
		return self.__value

	def __set__(self, instance, value):
		self.__value = value

	def __delete__(self,obg):
		del self.__value

class App:
	models = {}
	# app = SaveSelf()
	# db = SaveSelf()
	def __init__(self):
		self.app = Flask(__name__)
		self.app.config.from_object(Configurations)
		self.db =  SQLAlchemy(self.app)
		self.models= {}
		self.login_manager = LoginManager()
		self.login_manager.init_app(self.app)
		self.login_manager.login_viwe = 'login'


	def reg_blueprints(self):
		from rueng.routes import rueng
		from settings.routes import settings
		from home.routes import home
		self.app.register_blueprint(home,url_prefix='')
		self.app.register_blueprint(settings,url_prefix='/settings')
		self.app.register_blueprint(rueng,url_prefix='/rueng')

	def get_db(self):
		return self.db

	def get_app(self):
		return self.app

	def migrate(self):
		migrate = Migrate(self.app,self.db)
		manager = Manager(self.app)
		manager.add_command('db',MigrateCommand)
		return manager

	def add_model(model,obj):
		App.models.update({model:obj})

	def get_model(model):
		return App.models[model]
	def get_models_dict():
		return App.models

	def get_login_manager(self):
		return self.login_manager

app = App()


if __name__ == '__main__':
	app.reg_blueprints()
	app.get_app().run(debug=True,
		port = 8000,
		host = "0.0.0.0")

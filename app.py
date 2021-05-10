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
    MAX_CONTENT_LENGTH = 1024 * 1024 # Обьем в байтах 

# class SaveSelf:
# 	def __get__(self,instance, owner):
# 		return self.__value

# 	def __set__(self, instance, value):
# 		self.__value = value

# 	def __delete__(self,obg):
# 		del self.__value

# class App:
# 	# app = SaveSelf()
# 	# db = SaveSelf()
# 	def __new__(cls):
# 		if not hasattr(cls, 'instance'):
# 			print(cls)
# 			cls.instance = super(App, cls).__new__(cls)
# 		return cls.instance
app = Flask(__name__)
app.config.from_object(Configurations)
db =  SQLAlchemy(app)
		


def reg_blueprints(app):
	from rueng.routes import rueng
	from settings.routes import settings
	from home.routes import home
	app.register_blueprint(home,url_prefix='/')
	app.register_blueprint(settings,url_prefix='/settings')
	app.register_blueprint(rueng,url_prefix='/rueng')

	
migrate = Migrate(app,db)
manager = Manager(app)
manager.add_command('db',MigrateCommand)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_viwe = 'login'




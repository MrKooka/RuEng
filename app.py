import os 
from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from random import choice
from pprint import pprint
from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager
from flask_login import LoginManager
class Configurations:
	#server
	# SQLALCHEMY_DATABASE_URI='mysql+pymysql://kooka2:1@localhost:3306/rueng'
 	SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
 	SQLALCHEMY_TRACK_MODIFICATIONS = False
 	DEBUG = True
 	SECRET_KEY = os.environ.get('SECRET_KEY')
 	MAX_CONTENT_LENGTH = 1024 * 1024 # Обьем в байтах 


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




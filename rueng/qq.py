import sys
from pprint import pprint
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# from models import App 
# db = SQLAlchemy(app)
# d = {}

# def model(model):
	# d.update({''.format(model):model})

# def get_model(model):
	# return d[''.format(model)]
# print(get_model('app'))
# print(get_model('db'))
# import sys,os,inspect
# current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# parent_dir = os.path.dirname(current_dir)
# sys.path.insert(0, parent_dir)





# RuEng = App.get_model('RuEng')
# word_user = App.get_model('word_user')

# pprint(type(word_user))
# pprint(type(RuEng))
# pprint(type((RuEng.query.filter(RuEng.ru.contains('Дом')).first()).users))
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.automap import automap_base
# from sqlalchemy import create_engine
# engine = create_engine('mysql+pymysql://root:1@localhost:27017/test2')


# Base = automap_base()
# Base.prepare(engine,reflect=True)
# Session = sessionmaker(bind=engine)
# session = Session()
# user = Base.classes.user
# RuEng.query.filter_by(id='4').delete()
# pprint(dir(word_user.c))
# w = RuEng.query.join(RuEng.users).filter(RuEng.id == 1).all()
# print(type(w[0].id))
# w1 = session.query(word_user).filter(w[0].id)
# session.delete(w1)
# session.commit()
# print(type(word_user))
# c1 = session.query(word_user).all()
# .filter(Cities.id.contains('2')).first()
# pprint(type(c1))
# session.query(RuEng).filter(RuEng.id==1).delete()
class SaveSelf:
	def __get__(self,instance, owner):
		return self.__value

	def __set__(self, instance, value):
		self.__value = value

	def __delete__(self,obg):
		del self.__value



def sql():
	return 'lol'
class App:
	som = SaveSelf()
	def __init__(self):
		self.som = 'll'
		self.db = sql()
	def get_db(self):
		return self.db
	def set_som(self):
		pprint('set some ')
		self.som = 'l'
app = App()
appp =App()
pprint(app.som)
pprint(appp.som)


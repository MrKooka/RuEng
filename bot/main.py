import sys,os,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from flask import Flask,request
import requests
from models import RuEng,User,db,word_user
from pprint import pprint
from sqlalchemy import create_engine,inspect
from sqlalchemy.orm import sessionmaker
import polyglot
from polyglot.text import Text, Word
import logging
from sqlalchemy.sql import text,delete,and_
import telebot

# import logging.config 
# from log_settings import logger_config

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from flask_sqlalchemy import SQLAlchemy

requests_session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
requests_session.mount('http://', adapter)
requests_session.mount('https://', adapter)

# logging.config.dictConfig(logger_config)
# debug_logger = logging.getLogger('debug_logger')
debug_logger = logging.getLogger()
debug_logger.setLevel('DEBUG')
std_format = logging.Formatter(fmt = '{asctime} - {levelname} - {name} - {message}', style = '{')
console_handler = logging.StreamHandler()
console_handler.setFormatter(std_format)
debug_logger.addHandler(console_handler)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1@localhost:27017/rueng'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# engine = create_engine('mysql+pymysql://root:1@localhost:27017/rueng')
# Session = sessionmaker(bind=engine)
# session = Session()
# conn = engine.connect()
token = "1771178136:AAGu6w8JF8UkXSuKbo36_ozRTo2phCXYFnw"
#https://e50fc96bbb56.ngrok.io
from prettytable import PrettyTable

def send_msg(data):
	debug_logger.debug('Вход в send_msg')
	bot = telebot.TeleBot('1771178136:AAGu6w8JF8UkXSuKbo36_ozRTo2phCXYFnw')
	bot.send_message(data['chat_id'], data['text'],parse_mode=data['parse_mode'])

	# method = "sendMessage"
	# url = f"https://api.telegram.org/bot{token}/{method}"
	# requests_session.post(url, data=data)

def make_table(chat_id,utid):

	try:
		debug_logger.debug('Запуск add_word')
		user_id = User.query.filter(User.telegramid == utid).first().id
		allw = RuEng.query.filter(RuEng.users.any(id=user_id)).all()
	except:
		debug_logger.exception('Ошибка в make_table')
		data = {'chat_id':chat_id,'text':'Что то пошло не так, попробуй еще раз'}
		send_msg(data)
		return

	x = PrettyTable()
	x.field_names = ["id", "ru", "eng"]

	for i in allw:
		x.add_rows([[i.id,i.ru,i.eng]])
	# # data={'chat_id':chat_id,'text':"dfsdf"}
	data = {"chat_id": chat_id, 'text':f"```{x}```", 'parse_mode':'MarkdownV2'}
	send_msg(data)
	debug_logger.debug('add_word закончила работу')

def add_word(chat_id,ru,eng,utid,context=None):
	try:
		debug_logger.debug('Запуск add_word')

		user = User.query.filter(User.telegramid == utid).first()
		debug_logger.debug(f'Найден user: {user}')

		word= RuEng(ru=ru.lower(),eng=eng.lower(),context=context)
		debug_logger.debug(f'Создан экземпляр RuEng: {word}')


		word.users.append(user)
		db.session.add(word)
		db.session.commit()

		data = {'chat_id':chat_id,'text':'Слово добавлено','parse_mode':None}
		send_msg(data)
	except:
		# session.commit()
		debug_logger.exception('Ошибка в add-word')
		data = {'chat_id':chat_id,'text':'Что то пошло не так, попробуй еще раз'}
		send_msg(data)




def del_word(chat_id,word_id,utid):
	try:
		debug_logger.debug('Вход в функцию del_word')
		user_id = User.query.filter(User.telegramid == utid).first().id
		debug_logger.debug(f'Найден user_id:{user_id}')

		# sql = text(f'DELETE FROM word_user WHERE wid={word_id} AND uid={user_id};'.format(word_id=word_id,
																			 # user_id=user_id))
		# stmt = word_user.delete((and_(word_user.columns.uid==user_id,word_user.columns.wid == word_id)))
		stmt = delete(word_user).where(and_(word_user.columns.uid==user_id, word_user.columns.wid==word_id))
		db.engine.execute(stmt)
		db.session.commit()
		db.session.close()
		# db.session.expunge(stmt)

		data = {'chat_id':chat_id,'text':'Слово удалено','parse_mode':None}
		send_msg(data)
		debug_logger.debug('Выход из del_word')
	except:
		debug_logger.exception('Ошибка в dell_word')
		data={'chat_id':chat_id,'text':'что-то пошло не так  в del_word','parse_mode':None}
		send_msg(data)


def parse_message(chat_id,text,utid):
	text_list = text.split(':')

	if 'all' in text_list:
		make_table(chat_id,utid)

	elif 'add' in text_list: # ['add','ru' ,'eng']
		try:
			if  3 < len(text_list) >=4:
				ru = text_list[1]
				eng = text_list[2]
				context = text_list[3]
				add_word(chat_id,ru,eng,context,utid) 
				return
			ru = text_list[1]
			eng = text_list[2]
			add_word(chat_id,ru,eng,utid) 
		except:
			print('ошибка',text_list)


	elif 'del' in text_list:

		try:
			debug_logger.debug('del в сообщении, сообщение: {text_list}')
			word_id = text_list[1]
			del_word(chat_id,word_id,utid)
		except:
			data={'chat_id':chat_id,'text':'неверный формат'}
			send_msg(data)
	elif 'reset' in text_list:
		# db.session.commit()
		pprint(dir(db.session))
		data = {'chat_id':chat_id,'text':'lkek'}
		send_msg(data)
	else:
		text = text.strip().lower()
		word = Text(text)
		if word.language.code == 'ru':
			translate = session.query(RuEng).filter(RuEng.ru == 'word').first().eng
			data = {"chat_id": chat_id, 'text': translate,'parse_mode':None}
			send_all_msg(data)



	# send_all_msg(chat_id,allw)
	# if text == '/all':
 		# allw = session.query(RuEng).all()




@app.route("/", methods=["GET", "POST",'PUT'])
def receive_update():
	if request.method == "POST":
		try:
			debug_logger.debug(f'POST запрос от пользователя запрос:{request.json}')
			chat_id = request.json["message"]["chat"]["id"]
			text = request.json["message"]['text']
			utid = request.json["message"]['from']['id']
		# data = {'chat_id':chat_id,'text':'lolkek'}
		# db.session.expire_all()
			parse_message(chat_id,text,utid)
			debug_logger.debug('receive_update отработала')
		except:
			data = {'chat_id':'515854171','text':'Я не понял тебя мужик, попробуй еще раз','parse_mode':None}
			send_msg(data)	
			debug_logger.exception('Ошибка в receive_update')

	return {"ok": True}


if __name__ == '__main__':
	app.run(debug=True)
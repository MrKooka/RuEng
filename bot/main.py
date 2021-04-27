import sys,os,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from flask import Flask,request
import requests
from models import RuEng
from pprint import pprint
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+pymysql://root:1@localhost:27017/rueng')
Session = sessionmaker(bind=engine)
session = Session()
conn = engine.connect()
token = "1752025711:AAGNhNTZqn2B5ryID7YM6dICU5Ao4r517Pg"

app = Flask(__name__)

def send_message(chat_id,eng):

	method = "sendMessage"
	url = f"https://api.telegram.org/bot{token}/{method}"
	try:
		text = session.query(RuEng).filter_by(eng=eng).first().ru
	except:
		text = 'Такого у вас нет'
	print(text)
	data = {"chat_id": chat_id, "text": text}
	requests.post(url, data=data)
	session.commit()

def send_all_msg():
	method = "sendMessage"
	url = f"https://api.telegram.org/bot{token}/{method}"
	try:
		text = session.query(RuEng).all()
	except:
		text = 'Такого у вас нет'
	print(text)
	data = {"chat_id": chat_id, "text": text}
	requests.post(url, data=data)
	session.commit()
	

@app.route('/all')
def all():
	if request.method == "POST":
		pprint(request.json)
		chat_id = request.json["message"]["chat"]["id"]
		eng = request.json["message"]['text']
		send_message(chat_id)
	return {"ok": True}
@app.route("/", methods=["GET", "POST"])
def receive_update():
	if request.method == "POST":
		pprint(request.json)
		chat_id = request.json["message"]["chat"]["id"]
		eng = request.json["message"]['text']
		send_message(chat_id,eng)
	return {"ok": True}
if __name__ == '__main__':
	app.run()
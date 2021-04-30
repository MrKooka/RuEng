from flask import Flask,request,jsonify
import json
import requests
from pprint import pprint
app = Flask(__name__)
token = "1752025711:AAGNhNTZqn2B5ryID7YM6dICU5Ao4r517Pg"
URL = f"https://api.telegram.org/bot{token}/"
print(URL)
def write_json(data,filename = 'answer.json'):
	with open(filename,'w') as f:
		json.dump(data,f, indent=2, ensure_ascii=False)



def send_message(chat_id,text ='lol'):
	url = URL +'sendMessage'
	answer = {'chat_id':chat_id,'text':text}
	r = requests.post(url,answer)
	return r.json()

def parser():
	

@app.route('/',methods = ['POST','GET'])
def index():
	if request.method == 'POST':
		r = request.get_json()
		chat_id = r['message']['chat']['id']
		message = r['message']['text']
		print(chat_id,message)
		return jsonify(r)   
	return 'Hellow bot'


if __name__ == '__main__':
	app.run()
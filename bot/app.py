from flask import Flask
import json
import requests
app = Flask(__name__)
token = "1752025711:AAGNhNTZqn2B5ryID7YM6dICU5Ao4r517Pg"
URL = f"https://api.telegram.org/bot{token}/"
print(URL)
def write_json(data,filename = 'answer.json'):
	with open(filename,'w') as f:
		json.dump(data,f, indent=2, ensure_ascii=False)


def get_updates():
	url = URL +'getUpdates'
	r = requests.get(url)
	print(r)
	write_json(r.json)

def main():
	get_updates()
if __name__ == '__main__':
	main()
from flask import Flask, request
import telebot

app = Flask(__name__)
 
bot = telebot.TeleBot('1771178136:AAGu6w8JF8UkXSuKbo36_ozRTo2phCXYFnw')


@app.route("/", methods=["POST"])
def receive_update():
    chat_id = request.json["message"]["chat"]["id"]
    bot.send_message(chat_id, "Hello!")
    return "ok"


if __name__ == "__main__":
    app.run()
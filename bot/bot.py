import logging
import os
import sys
import time
from collections import defaultdict
from io import StringIO

import requests
from telegram import KeyboardButton, ReplyKeyboardMarkup, ParseMode, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

LINK_TO_BOT = 't.me/bot_terter_bot'

TOKEN = os.environ['API_TOKEN']


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.ERROR
)

TASKS = {
    "decorator": {
        "descr": """*Задание \@decorator*
Написать class Decorator\, который будет кэшировать последние 5 значений возвращаемых из функции на которую он повешен\.
У каждой функции свой пул для кэша\.

По готовности, загрузите файл""",
        "test_cases": open('tasks/decorator.py').read()
    }
}


def main_menu_keyboard():
    keyboard = [
        [KeyboardButton("decorator")],
        [KeyboardButton("Какое активное задание?")],
    ]
    return ReplyKeyboardMarkup(keyboard)


def start(update, context):
    if update.message is not None:
        chat_id = update.message.chat_id
    else:
        chat_id = update.callback_query.message.chat_id

    context.bot.send_message(
        chat_id=chat_id,
        text='Привет\nЯ бот который может прогонять тесты по заданию.\nВыбери задание =)',
        reply_markup=main_menu_keyboard()
    )


CONTEXT = {}


def user_input(update: Update, context: CallbackContext):
    message_text = update.message.text
    user_id = update.effective_user.id

    if message_text == "Какое активное задание?":
        if user_id in CONTEXT:
            text = TASKS[CONTEXT[user_id]]['descr']
        else:
            text = "Никакого задания не выбрано \=\("
    else:
        if message_text in TASKS:
            CONTEXT[user_id] = message_text
            text = TASKS[message_text]['descr']
        else:
            text = "Sorry unknown task"

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=text,
        parse_mode=ParseMode.MARKDOWN_V2
    )

test_context = {}


def file_input(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    f = update.message.document

    if f.file_name.split('.')[-1] != 'py':
        return context.bot.send_message(
            chat_id=update.message.chat_id,
            text="Файл неподдерживаемого формата \=\( ",
            parse_mode=ParseMode.MARKDOWN_V2
        )

    if not user_id in CONTEXT:
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text="Вы не выбрали задание \=\( ",
            parse_mode=ParseMode.MARKDOWN_V2
        )
    else:
        get_file_link = f"https://api.telegram.org/bot{TOKEN}/getFile?file_id={update.message.document.file_id}"
        response = requests.get(get_file_link)
        data = response.json()

        file_link = f"https://api.telegram.org/file/bot{TOKEN}/{data['result']['file_path']}"

        res = requests.get(file_link)
        text = ""

        file_text = res.text
        uid = int(time.time())
        test_context[uid] = defaultdict(list)

        codeOut = StringIO()
        codeErr = StringIO()

        old_stdout = sys.stdout
        old_stderr = sys.stderr

        sys.stdout = codeOut
        sys.stderr = codeErr

        file_text += "\n\n\n" + TASKS[CONTEXT[user_id]]['test_cases']

        err_str = ""
        try:
            exec(file_text, {"test_context": test_context, "uid": uid})
        except Exception as e:
            err = str(e)
            err_str += "\n" + err

        sys.stdout = old_stdout
        sys.stderr = old_stderr

        err = codeErr.getvalue() + err_str

        i = 1
        for k, res in test_context[uid].items():
            text += f"\n{i}. {k}\n"
            i += 1
            for j, r in enumerate(res):
                text += f"Case {j + 1} : {'✅' if r else '❌'}\n"

        if err:
            text += f"!!!!! ⚠️ ОШИБКА ⚠️ !!!!\n{err_str}\n\nNOTE: all tests running in python-3.7.9 env"

        # s = codeOut.getvalue()
        # print("output:\n%s" % s)

        codeOut.close()
        codeErr.close()

        # TODO: check file
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text=text,
        )


def main():
    print('run start')
    updater = Updater(token=TOKEN, use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))

    dispatcher.add_handler(MessageHandler(Filters.text, user_input))
    dispatcher.add_handler(MessageHandler(Filters.document, file_input))

    print('run loop')
    updater.start_polling()


print('start')
if __name__ == '__main__':
    main()

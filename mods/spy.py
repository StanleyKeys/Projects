from telegram import Update
from telegram.ext import CommandHandler, ContextTypes


def log(update: Update, context: ContextTypes.DEFAULT_TYPE):                                        # Запись Лога в файл db.csv

    file = open('db.csv', 'a')
    file.write(f'{update.effective_user.first_name}, {update.effective_user.id}, {update.message.text}\n')
    file.close()

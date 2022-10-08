from ast import Break
import sys
import telebot                                                 #  https://pypi.org/project/pyTelegramBotAPI/  
from telebot import types
from telegram import Update
from telegram.ext import Updater, CommandHandler, ContextTypes
import datetime
import pytube               # pip install pytube
import weatherCommand
import os, glob
import time
token = 'TOKEN'
bot = telebot.TeleBot(token)

name = ''
surname = ''
age = 0
url = ''
resolution = ''
helpResult = ''

#======================================================================================= Функции скачивания с Ютуба
def YouTube_Resolution(message):
    global url
    url = f'{message.text}'
    
    bot.send_message(message.from_user.id, f'В каком качестве?\n1.360p\n2.480p\n3.720p')
    bot.register_next_step_handler(message, YouTube_Download)

def YouTube_Download(message):
    global link
    global resolution
    global stream
    link = pytube.YouTube(url)
    resolution = message.text
    if (resolution == 1) or (resolution == '1'):
        stream = link.streams.get_by_itag(134)
    if (resolution == 2) or (resolution == '2'):
        stream = link.streams.get_by_itag(135)
    if (resolution == 3) or (resolution == '3'):
        stream = link.streams.get_by_itag(136)
    stream.download('Downloads')
    for filename in os.listdir("F:\GeekBrains\TestFold\JarvisBot\Downloads"):
            videoName = filename
    downloadVideo = open(f'F:\GeekBrains\TestFold\JarvisBot\Downloads\{videoName}', 'rb')
    bot.send_video(message.from_user.id, downloadVideo)
    downloadVideo.close()
    time.sleep(2)
    for file in glob.glob("F:\GeekBrains\TestFold\JarvisBot\Downloads\*"):
        os.remove(file)
        
#==============================================================================
def CheckCity(message):
    global resultCity
    if message.text == '1':
        city_id = 524901 # Moscow  
    if message.text == '2':
        city_id = 519690 # SpB
    if message.text == '3':
        city_id = 1496747 # Novosibirsk
    if message.text == '4':
        city_id = 2023469 # Irkutsk
    if message.text == '5':
        city_id = 2013348 # Vladivostok
    if message.text == '6':
        city_id = 2022890 # Khabarovsk
    if message.text == '7':
        city_id = 2122104 # Petropavlovsk-Kamchatsky
    resultCity = city_id
    bot.send_message(message.from_user.id, 'Погода: \n1.Сейчас \n2.Прогноз')
    bot.register_next_step_handler(message, weatherChoice)
    

def weatherChoice(message):     
    if  message.text == '1': 
        result = weatherCommand.request_current_weather(resultCity)
        bot.send_message(message.from_user.id, f'{result}')
    if  message.text == '2': 
        result = weatherCommand.request_forecast(resultCity)
        bot.send_message(message.from_user.id, f'{result}')

#====================================================================================   Начальные Функции
@bot.message_handler(content_types=['text'])

def start(message):
    if message.text == '/start':
        bot.send_message(message.from_user.id, f'Привет, {name}! Я Джарвис! Хочешь узнать что я умею?😃')
        bot.register_next_step_handler(message, helpChoice)

    if message.text == '/dialog':
        bot.send_message(message.from_user.id, 'Привет! А как тебя зовут?')
        bot.register_next_step_handler(message, dialog1)

    if message.text == '/sum':
        bot.send_message(message.from_user.id, 'Введите числа через пробел: ')
        bot.register_next_step_handler(message, Sum_Command)

    if message.text =='/download':
        bot.send_message(message.from_user.id, 'Введите ссылку "https://..."')
        bot.register_next_step_handler(message, YouTube_Resolution)
    if message.text =='/help':
        bot.send_message(message.from_user.id, 'Вот что я могу: \n/help - Список команд \
            \n/sum - Складывание\n/dialog - общение со мной :)\n/download - Скачать с YouTube\n/weather - Погода')

    if message.text =='/weather':
        bot.send_message(message.from_user.id, 'В каком городе интересует погода?\n1.Москва\n2.Санк-Петербург\n3.Новосибирск\n4.Иркутск \
            \n5.Владивосток \n6.Хабаровск \n7.Петропавловск-Камчатский')
        bot.register_next_step_handler(message, CheckCity)
    
    if message.text =='/shutdown':              #   вырубить бота дистанционно
        bot.stop_polling()
        
    
#=================================================================================== Сложение чисел      
def Sum_Command(message):
    msg = message.text
    items = msg.split()
    x = int(items[0])
    y = int(items[1])
    bot.send_message(message.from_user.id, f'{x} + {y} = {x+y}')
#===================================================================================  Простой Диалог
def dialog1(message):
    global name
    name = message.text
    bot.send_message(message.from_user.id, 'Какая у тебя фамилия?')
    bot.register_next_step_handler(message, dialog2)

def dialog2(message):
    global surname
    surname = message.text
    bot.send_message(message.from_user.id, 'Сколько тебе лет?')
    bot.register_next_step_handler(message, dialog3)

def dialog3(message):
    global name
    age = message.text
    bot.send_message(message.from_user.id, f'Приятно познакомиться, {name}! Я Джарвис! как твои дела?')

#========================================================================================   Функция помощи
def helpChoice(message):
    
    helpResult = message.text
    if (helpResult == 'да') or (helpResult == 'Да'):
        bot.send_message(message.from_user.id, f'Вот что я могу: \n/help - Список команд \
            \n/sum - Складывание\n/dialog - общение со мной :)\n/download - Скачать с YouTube\n/weather - Погода')
    if (helpResult == 'нет') or (helpResult == 'Нет'):
        bot.send_message(message.from_user.id, f'Ну ладно. пойду дальше учить новые фичи ;)')
#=====================================================================================


print('bot starts')
bot.polling(non_stop=True, interval=0)


import os
import telebot
from telebot import types
import subprocess
import sys
# Создаем экземпляр бота
bot = telebot.TeleBot('6454987961:AAGPVafl1tJf3NJ-fW_NpgW7TdFHUVtiyCI')
# Функция, обрабатывающая команду /start
@bot.message_handler(commands=["start"])
def start(m, res=False):
        #bot.send_message(m.chat.id, 'Я на связи. Напиши мне что-нибудь)')
        # Добавляем две кнопки
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1=types.KeyboardButton("Обновить сервера")
        item2=types.KeyboardButton("Домой")
        markup.add(item1)
        markup.add(item2)
        bot.send_message(m.chat.id, 'Нажми обновить', reply_markup=markup)
# Получение сообщений от юзера
@bot.message_handler(content_types=["text"])
def handle_text(message):
    if message.text.strip() == 'Обновить сервера' :
        bot.send_message(message.chat.id, 'Вы написали: ' + message.text)
    elif message.text.strip() == 'Домой' :
        #m=os.system("date")
        #print(m)
        #bot.send_message(message.chat.id, os.system("date"))
        #bot.send_message(message.chat.id, os.popen("ls -la").read())
        #bot.send_message(message.chat.id, os.("ls -la").read())
        bot.send_message(message.chat.id, subprocess.run(["ls", "-l"]))
        #print(os.popen("ls -l").read())
        #@bot.message_handler(commands=["start"])
# Запускаем бота
bot.polling(none_stop=True, interval=0)
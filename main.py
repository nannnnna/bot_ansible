import logging
import os
import subprocess

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

load_dotenv()
logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv('TOKEN')
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton("Обновить сервера")
button2 = KeyboardButton("Домой")
main_keyboard.add(button1, button2)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Выберите действие", reply_markup=main_keyboard)

@dp.message_handler(lambda message: message.text == 'Обновить сервера')
async def choose_server(message: types.Message):
    inline_kb = InlineKeyboardMarkup()
    servers = ["Server1", "Server2", "Server3"]
    for server in servers:
        btn = InlineKeyboardButton(server, callback_data=server)
        inline_kb.add(btn)
    await message.reply("Выберите сервер для обновления", reply_markup=inline_kb)

@dp.callback_query_handler(lambda c: c.data in ["Server1", "Server2", "Server3"])
async def process_callback(callback_query: types.CallbackQuery):
    server = callback_query.data
    # Здесь добавьте код для обновления сервера
    await bot.send_message(callback_query.from_user.id, f"Сервер {server} обновлен")

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)

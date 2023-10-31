import logging
import os
import subprocess

from dotenv import load_dotenv
from aiogram.types import CallbackQuery
from aiogram import Bot, types
from aiogram.dispatcher import FSMContext, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

load_dotenv()
logging.basicConfig(level=logging.INFO)

class Form(StatesGroup):
    waiting_for_server_name = State()
    waiting_for_branch_name = State()

TOKEN = os.getenv('TOKEN')
storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())
ALLOWED_USERS = ['anastaaaaaass', 'MrHime', 'Asterpy', 'nikalayrx', 'mocart_work', 'AlexMocart']


main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton("Обновить сервера")
button2 = KeyboardButton("Заново")
main_keyboard.add(button1, button2)


@dp.message_handler(commands=['start'], state="*")
async def cmd_start(message: types.Message):
    user_username = message.from_user.username  
    
    if user_username not in ALLOWED_USERS:
        await message.reply("Извините, у вас нет доступа к этому боту.")
        return

    await message.reply("Выберите действие:", reply_markup=main_keyboard)
    
@dp.message_handler(lambda message: message.text.lower() == 'заново', state="*")
async def restart_process(message: types.Message, state: FSMContext):
    await state.finish()  
    await process_start(message)  


@dp.message_handler(lambda message: message.text.lower() == 'обновить сервера', state="*")
async def update_servers(message: types.Message, state: FSMContext):
    await Form.waiting_for_server_name.set()
    await message.reply("Введите название сервера и ветку в формате сервер:ветка:")

@dp.message_handler(state=Form.waiting_for_server_name, content_types=types.ContentTypes.TEXT)
async def process_server_and_branch(message: types.Message, state: FSMContext):
    servers_and_branches = message.text.split(';')

    for pair in servers_and_branches:
        server_and_branch = pair.split(':')

        # Проверяем, что для каждой пары указаны сервер и ветка
        if len(server_and_branch) != 2:
            await message.reply("Пожалуйста, введите данные в формате сервер:ветка;сервер:ветка")
            return
        else:
            await message.reply("Процесс запущен, подождите...")

        async with state.proxy() as data:
            data['server_name'] = server_and_branch[0].strip() 
            data['branch_name'] = server_and_branch[1].strip() 

       
        if data['server_name'] == 'crm5':
            playbook_name = 'update_crm5.yaml'
        elif data['server_name'] in ['crmnew', 'crmnew3']:
            playbook_name = 'update_crmtarget.yaml'
        else:
            playbook_name = 'update_crm.yaml'

        
        command = f"ansible-playbook /etc/ansible/{playbook_name} -e 'branch={data['branch_name']}' -l '{data['server_name']}'"
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode == 0:
            await message.reply(f"Сервер {data['server_name']} успешно обновлен в ветке {data['branch_name']}.")
        else:
            await message.reply(f"Ошибка при обновлении сервера {data['server_name']} в ветке {data['branch_name']}:\n{stderr.decode()}")

    await state.finish()


if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
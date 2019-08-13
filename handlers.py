from aiogram import types
from main import dp
from dialogs import MainDialog


@dp.message_handler(commands='start', state='*')
async def start(message: types.Message):
    await message.reply('Привет! Как тебя зовут?')
    await MainDialog.enter_name.set()

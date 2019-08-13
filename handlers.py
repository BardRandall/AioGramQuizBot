from aiogram import types
from aiogram.dispatcher import FSMContext

from main import dp
from dialogs import MainDialog


@dp.message_handler(commands='start', state='*')
async def start(message: types.Message):
    await message.answer('Привет! Как тебя зовут?')
    await MainDialog.enter_name.set()


@dp.message_handler(state=MainDialog.enter_name)
async def enter_name(message: types.Message, state: FSMContext):
    async with state.proxy() as storage:
        storage['name'] = message.text
    await message.answer(f'Приятно познакомиться,  {message.text}. А сколько тебе лет?')
    await MainDialog.enter_age.set()

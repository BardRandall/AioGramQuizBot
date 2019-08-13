from aiogram import types
from aiogram.dispatcher import FSMContext

from main import bot, dp, questions
from dialogs import MainDialog
from quiz import send_question


@dp.message_handler(commands='start', state='*')
async def start(message: types.Message):
    await message.answer('Привет! Как тебя зовут?')
    await MainDialog.enter_name.set()


@dp.message_handler(state=MainDialog.enter_name)
async def enter_name(message: types.Message, state: FSMContext):
    async with state.proxy() as storage:
        storage['name'] = message.text
    await message.answer(f'Приятно познакомиться, {message.text}. А сколько тебе лет?')
    await MainDialog.enter_age.set()


@dp.message_handler(state=MainDialog.enter_age)
async def enter_age(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('Введите корректный возраст')
        return
    if not 1 <= int(float(message.text)) <= 100:
        await message.answer('Введите корректный возраст')
        return
    async with state.proxy() as storage:
        storage['age'] = message.text
        storage['current_question'] = 0
        await message.answer(f'Ну что, {storage["name"]} {storage["age"]} лет, начнём игру')
        await send_question(bot, message.chat.id, questions[storage['current_question']])
    await MainDialog.quiz.set()


from aiogram import types
from aiogram.dispatcher import FSMContext

from main import bot, dp, questions
from dialogs import MainDialog
from quiz import send_question, factory


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


@dp.message_handler(state=MainDialog.quiz)
async def quiz_process(message: types.Message, state: FSMContext):
    async with state.proxy() as storage:
        ### Здесь код повторяется, но мне лень вынести в функцию ###
        # TODO refactoring
        current_question = questions[storage['current_question']]
        if message.text not in current_question.answers:
            await message.answer('Выберите один из предложенных ответов')
            return
        if not current_question.is_right(message.text):
            await message.answer('Неправильный ответ, попробуйте еще раз')
        else:
            await message.answer(text='Верно! Ответишь на следующий?',
                                 reply_markup=types.ReplyKeyboardRemove())
            storage['current_question'] += 1
            if storage['current_question'] >= len(questions):
                await message.answer(
                    'Ой, вопросы для вас закончились, приходите завтра или пройдите заново, нажав /start',
                    reply_markup=types.ReplyKeyboardRemove())
                await MainDialog.win.set()
                return
            await send_question(bot, message.chat.id, questions[storage['current_question']])


@dp.message_handler(state=MainDialog.win)
async def win(message: types.Message):
    await bot.send_message(message.chat.id,
                           text='Ой, вопросы для вас закончились, приходите завтра или пройдите заново, нажав /start')


@dp.callback_query_handler(factory.filter())
async def callback_handler(query: types.CallbackQuery, state: FSMContext):
    await query.answer()
    async with state.proxy() as storage:
        ### Здесь код повторяется, но мне лень вынести в функцию ###
        # TODO refactoring
        current_question = questions[storage['current_question']]
        if query.data not in current_question.answers:
            await query.answer('Выберите один из предложенных ответов')
            return
        if not current_question.is_right(query.data):
            await bot.send_message(query.message.chat.id, text='Неправильный ответ, попробуйте еще раз')
        else:
            await bot.send_message(query.message.chat.id, text='Верно! Ответишь на следующий?',
                                   reply_markup=types.ReplyKeyboardRemove())
            storage['current_question'] += 1
            if storage['current_question'] >= len(questions):
                await bot.send_message(query.message.chat.id,
                                       text='Ой, вопросы для вас закончились, приходите завтра или пройдите заново, нажав /start',
                                       reply_markup=types.ReplyKeyboardRemove())
                MainDialog.win.set()
                return
            await send_question(bot, query.message.chat.id, questions[storage['current_question']])

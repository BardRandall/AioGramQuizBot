from aiogram import types
from aiogram.types import KeyboardButton


class Question:

    def __init__(self, question, answers, right_answer, keyboard_type):
        self.question = question
        self.answers = answers
        self.right_answer = right_answer
        self.keyboard_type = keyboard_type

    def is_right(self, user_answer):
        return user_answer == self.answers[self.right_answer]


async def send_question(bot, chat_id, question):
    keyboard_markup = types.ReplyKeyboardRemove()
    if question.keyboard_type or True:  # TODO other type of keyboard
        keyboard_markup = types.ReplyKeyboardMarkup(row_width=2)
        for q in question.answers:
            keyboard_markup.add(KeyboardButton(q))
    await bot.send_message(chat_id, text=question.question, reply_markup=keyboard_markup)

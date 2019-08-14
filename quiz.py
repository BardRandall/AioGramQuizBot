from aiogram import types
from aiogram.types import KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.callback_data import CallbackData

factory = CallbackData('quiz_answers', 'number')


class Question:

    def __init__(self, question, answers, right_answer, keyboard_type):
        self.question = question
        self.answers = answers
        self.right_answer = right_answer
        self.keyboard_type = keyboard_type

    def is_right(self, user_answer):
        return user_answer.lower() == self.answers[self.right_answer].lower()

    def is_right_by_index(self, user_index):
        return self.is_right(self.answers[user_index])


async def send_question(bot, chat_id, question):
    if question.keyboard_type == 0:
        keyboard_markup = types.ReplyKeyboardMarkup(row_width=2)
        for q in question.answers:
            keyboard_markup.add(KeyboardButton(q))
    elif question.keyboard_type == 1:
        keyboard_markup = InlineKeyboardMarkup(row_width=2)
        for i, q in enumerate(question.answers):
            keyboard_markup.add(
                InlineKeyboardButton(text=q, callback_data=factory.new(number=i))
            )
    else:
        keyboard_markup = ReplyKeyboardRemove()
    await bot.send_message(chat_id, text=question.question, reply_markup=keyboard_markup)

from aiogram.dispatcher.filters.state import StatesGroup, State


class MainDialog(StatesGroup):

    enter_name = State()
    enter_age = State()
    quiz = State()
    win = State()

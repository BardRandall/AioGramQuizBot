import json
import logging

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from core.quiz import Question

logging.basicConfig(level=logging.DEBUG)

TOKEN = "617318489:AAGuwWvdS8KG5YUSoq9Us5s6FHOPOMmmdys"
bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=RedisStorage2(host='localhost', port=6379))
dp.middleware.setup(LoggingMiddleware())

questions = []
with open("data.json") as f:
    raw_data = json.load(f)
    for q in raw_data:
        questions.append(Question(**q))

if __name__ == "__main__":
    executor.start_polling(dp)

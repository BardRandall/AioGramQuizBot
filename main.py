import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

logging.basicConfig(level=logging.DEBUG)

TOKEN = '617318489:AAGuwWvdS8KG5YUSoq9Us5s6FHOPOMmmdys'
bot = Bot(TOKEN)
dp = Dispatcher(bot)
storage = MemoryStorage()
dp.middleware.setup(LoggingMiddleware())


if __name__ == '__main__':
    executor.start_polling(dp)

from aiogram import Bot, Dispatcher
from Tasker_bot.app.config_reader import load_config
from aiogram.contrib.fsm_storage.memory import MemoryStorage


config = load_config('config/bot.ini')
bot: Bot = Bot(token=config.tg_bot.token)
dp: Dispatcher = Dispatcher(bot, storage=MemoryStorage())

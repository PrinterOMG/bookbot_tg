from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import config
from utils.db_api import UsersWorker, LanguagesWorker, ReferralWorker

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

users_worker = UsersWorker(db_name=config.DB_NAME, password=config.DB_PASSWORD, username=config.DB_USER, host=config.DB_HOST)
languages_worker = LanguagesWorker(db_name=config.DB_NAME, password=config.DB_PASSWORD, username=config.DB_USER, host=config.DB_HOST)
referral_worker = ReferralWorker(db_name=config.DB_NAME, password=config.DB_PASSWORD, username=config.DB_USER, host=config.DB_HOST)

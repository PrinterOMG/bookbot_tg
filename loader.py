from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import config
from utils.db_api import UsersWorker, LanguagesWorker, ReferralWorker, SubPricesWorker, PromocodesWorker, SettingsWorker
from utils.db_api import QuestionsWorker, BooksWorker, SubscribesWorker, OperationsWorker

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

users_worker = UsersWorker(db_name=config.DB_NAME, password=config.DB_PASSWORD, username=config.DB_USER, host=config.DB_HOST)
languages_worker = LanguagesWorker(db_name=config.DB_NAME, password=config.DB_PASSWORD, username=config.DB_USER, host=config.DB_HOST)
referral_worker = ReferralWorker(db_name=config.DB_NAME, password=config.DB_PASSWORD, username=config.DB_USER, host=config.DB_HOST)
subprices_worker = SubPricesWorker(db_name=config.DB_NAME, password=config.DB_PASSWORD, username=config.DB_USER, host=config.DB_HOST)
promo_worker = PromocodesWorker(db_name=config.DB_NAME, password=config.DB_PASSWORD, username=config.DB_USER, host=config.DB_HOST)
settings_worker = SettingsWorker(db_name=config.DB_NAME, password=config.DB_PASSWORD, username=config.DB_USER, host=config.DB_HOST)
questions_worker = QuestionsWorker(db_name=config.DB_NAME, password=config.DB_PASSWORD, username=config.DB_USER, host=config.DB_HOST)
books_worker = BooksWorker(db_name=config.DB_NAME, password=config.DB_PASSWORD, username=config.DB_USER, host=config.DB_HOST)
subscribes_worker = SubscribesWorker(db_name=config.DB_NAME, password=config.DB_PASSWORD, username=config.DB_USER, host=config.DB_HOST)
operations_worker = OperationsWorker(db_name=config.DB_NAME, password=config.DB_PASSWORD, username=config.DB_USER, host=config.DB_HOST)

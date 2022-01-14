from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from loader import books_worker, languages_worker
from .callbacks import navigation_callback, fundraising_callback


async def get_fundraising_keyboard(user_id):
    text = languages_worker.get_text_on_user_language(user_id, "backButton")

    books = books_worker.get_all_books()

    keyboard = [[InlineKeyboardButton(book["name"], callback_data=fundraising_callback.new(book["bookId"]))] for book in books]
    keyboard.append([InlineKeyboardButton(text["backButton"], callback_data=navigation_callback.new("main"))])

    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)

    return keyboard

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import languages_worker, books_worker


async def get_fund_book_keyboard(user_id, book_id, price):
    text = languages_worker.get_text_on_user_language(user_id, "fundBookMenu")
    book = books_worker.get_book(book_id)



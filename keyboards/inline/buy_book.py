from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from loader import languages_worker
from .callbacks import buy_book_callback, navigation_callback


async def get_book_buy_keyboard(user_id, link, price):
    text = languages_worker.get_text_on_user_language(user_id, "buyBookButton, backButton")

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text["buyBookButton"], callback_data=buy_book_callback.new(link, price))
        ],
        [
            InlineKeyboardButton(text["backButton"], callback_data=navigation_callback.new("main"))
        ]
    ])

    return keyboard

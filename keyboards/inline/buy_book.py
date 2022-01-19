from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from loader import languages_worker
from .callbacks import buy_book_callback, navigation_callback


async def get_book_buy_keyboard(user_id, book_id):
    text = languages_worker.get_text_on_user_language(user_id, "payButton, backButton")

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text["payButton"], callback_data=buy_book_callback.new(book_id))
        ],
        [
            InlineKeyboardButton(text["backButton"], callback_data=navigation_callback.new("main"))
        ]
    ])

    return keyboard

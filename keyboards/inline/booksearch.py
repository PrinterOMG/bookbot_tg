from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from loader import languages_worker
from keyboards.inline.callbacks import navigation_callback, search_callback


async def get_search_keyboard(user_id):
    text = languages_worker.get_text_on_user_language(user_id, "yearButton, genreButton, authorButton, titleButton, backButton")

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text["titleButton"], callback_data=search_callback.new("title"))
        ],
        [
            InlineKeyboardButton(text["genreButton"], callback_data=search_callback.new("genre"))
        ],
        [
            InlineKeyboardButton(text["authorButton"], callback_data=search_callback.new("author"))
        ],
        [
            InlineKeyboardButton(text["yearButton"], callback_data=search_callback.new("year"))
        ],
        [
            InlineKeyboardButton(text["backButton"], callback_data=navigation_callback.new("main"))
        ]
    ])

    return keyboard

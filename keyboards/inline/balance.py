from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from .callbacks import navigation_callback
from loader import languages_worker


def get_balance_keyboard(user_id):
    text = languages_worker.get_text_on_user_language(user_id, "topUpButton, backButton")

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text["topUpButton"], callback_data="top_up")
        ],
        [
            InlineKeyboardButton(text["backButton"], callback_data=navigation_callback.new("main"))
        ]
    ])

    return keyboard

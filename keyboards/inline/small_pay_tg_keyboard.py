from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from loader import languages_worker
from .callbacks import navigation_callback, telegram_pay_callback


async def get_small_pay_tg_keyboard(user_id, amount):
    text = languages_worker.get_text_on_user_language(user_id, "payButton, cancelButton")

    keyboard = [
        [
            InlineKeyboardButton(text["payButton"], callback_data=telegram_pay_callback.new(user_id, amount))
        ],
        [
            InlineKeyboardButton(text["cancelButton"], callback_data=navigation_callback.new("main"))
        ]
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)

    return keyboard

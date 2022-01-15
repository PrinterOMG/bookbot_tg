from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from loader import languages_worker
from .callbacks import navigation_callback, check_callback


async def get_pay_keyboard(user_id, order_id, link, what, amount, sub_id):
    text = languages_worker.get_text_on_user_language(user_id, "payButton, cancelButton, checkPayButton")  # dict\

    keyboard = [
        [
            InlineKeyboardButton(text["payButton"], url=link)
        ],
        [
            InlineKeyboardButton(text["checkPayButton"], callback_data=check_callback.new(what, order_id, amount, sub_id))
        ],
        [
            InlineKeyboardButton(text["cancelButton"], callback_data=navigation_callback.new("main"))
        ]
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)

    return keyboard

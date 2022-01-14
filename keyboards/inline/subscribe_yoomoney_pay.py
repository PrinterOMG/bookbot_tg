from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from loader import languages_worker
from .callbacks import navigation_callback, yoomoney_sub_callback


async def get_yoomoney_pay_keyboard(user_id, amount):
    text = languages_worker.get_text_on_user_language(user_id, "cancelButton")
    keyboard = [
        [
            InlineKeyboardButton("Bank card", callback_data=yoomoney_sub_callback.new("bank_card", amount))
        ],
        [
            InlineKeyboardButton("Apple Pay", callback_data=yoomoney_sub_callback.new("apple_pay", amount))
        ],
        [
            InlineKeyboardButton("Goggle Pay", callback_data=yoomoney_sub_callback.new("google_pay", amount))
        ],
        [
            InlineKeyboardButton("YooMoney", callback_data=yoomoney_sub_callback.new("yoo_money", amount))
        ],
        [
            InlineKeyboardButton(text["cancelButton"], callback_data=navigation_callback.new("subscribes"))
        ]
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)

    return keyboard

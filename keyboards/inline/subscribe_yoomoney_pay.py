from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from loader import languages_worker
from .callbacks import navigation_callback, yoomoney_sub_callback


async def get_yoomoney_pay_keyboard(user_id, amount, sub_id):
    text = languages_worker.get_text_on_user_language(user_id, "cancelButton")
    keyboard = [
        [
            InlineKeyboardButton("Bank card", callback_data=yoomoney_sub_callback.new("bank_card", amount, sub_id))
        ],
        [
            InlineKeyboardButton("Apple Pay", callback_data=yoomoney_sub_callback.new("apple_pay", amount, sub_id))
        ],
        [
            InlineKeyboardButton("Goggle Pay", callback_data=yoomoney_sub_callback.new("google_pay", amount, sub_id))
        ],
        [
            InlineKeyboardButton("YooMoney", callback_data=yoomoney_sub_callback.new("yoo_money", amount, sub_id))
        ],
        [
            InlineKeyboardButton(text["cancelButton"], callback_data=navigation_callback.new("subscribes"))
        ]
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)

    return keyboard

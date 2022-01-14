from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from loader import languages_worker
from .callbacks import navigation_callback, payment_callback


async def get_payment_keyboard(user_id, for_subs=False, value=0, back="main"):
    text = languages_worker.get_text_on_user_language(user_id, "telegramPayButton, yookassaButton, paypalButton, sbpButton, backButton")

    if for_subs:
        keyboard = [
            [
                InlineKeyboardButton(text["yookassaButton"], callback_data=payment_callback.new("sub", value, "yoomoney_sub"))
            ],
            [
                InlineKeyboardButton(text["paypalButton"], callback_data=payment_callback.new("sub", value, "paypal_sub"))
            ]
        ]
    else:
        keyboard = [
            [
                InlineKeyboardButton(text["telegramPayButton"], callback_data=payment_callback.new("topup", value, "telegram"))
            ],
            [
                InlineKeyboardButton(text["yookassaButton"], callback_data=payment_callback.new("topup", value, "yoomoney"))
            ],
            [
                InlineKeyboardButton(text["paypalButton"], callback_data=payment_callback.new("topup", value, "paypal"))
            ],
            # [
            #     InlineKeyboardButton(text["sbpButton"], callback_data=payment_callback.new("topup", value, "sbp"))
            # ]
        ]

    keyboard.append([InlineKeyboardButton(text["backButton"], callback_data=navigation_callback.new(back))])

    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)

    return keyboard

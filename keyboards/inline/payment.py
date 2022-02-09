from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from loader import languages_worker
from .callbacks import navigation_callback, payment_callback, yoomoney_sub_callback


async def get_payment_keyboard(user_id, for_subs=False, value=0, back="main", id=0):
    text = languages_worker.get_text_on_user_language(user_id, "telegramPayButton, yookassaButton, paypalButton, sbpButton, backButton")

    if for_subs:
        keyboard = [
            # [
            #     InlineKeyboardButton(text["yookassaButton"], callback_data=payment_callback.new("sub", value, "yoomoney_sub", id))
            # ],
            [
                InlineKeyboardButton(text["yookassaButton"], callback_data=yoomoney_sub_callback.new("bank_card", value, id))
            ],
            # [
            #     InlineKeyboardButton(text["paypalButton"], callback_data=payment_callback.new("sub", value, "paypal_sub", id))
            # ]
        ]
    else:
        keyboard = [
            [
                InlineKeyboardButton(text["telegramPayButton"], callback_data=payment_callback.new("topup", value, "telegram", 0))
            ],
            [
                InlineKeyboardButton(text["yookassaButton"], callback_data=payment_callback.new("topup", value, "yoomoney", 0))
            ],
            # [
            #     InlineKeyboardButton(text["paypalButton"], callback_data=payment_callback.new("topup", value, "paypal", 0))
            # ],
            # [
            #     InlineKeyboardButton(text["sbpButton"], callback_data=payment_callback.new("topup", value, "sbp"))
            # ]
        ]

    keyboard.append([InlineKeyboardButton(text["backButton"], callback_data=navigation_callback.new(back))])

    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)

    return keyboard

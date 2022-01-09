from loader import languages_worker

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .callbacks import navigation_callback


async def get_main_keyboard(user_id):
    text_list = "infoButton, subscribesButton, balanceButton, makeQuestionButton, booksArchiveButton, " \
                "fundraisingButton, changeLanguageButton"
    text = languages_worker.get_text_on_user_language(user_id, text_list)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text["subscribesButton"], callback_data=navigation_callback.new("subscribes")),
            InlineKeyboardButton(text["balanceButton"], callback_data=navigation_callback.new("balance"))
        ],
        [
            InlineKeyboardButton(text["fundraisingButton"], callback_data=navigation_callback.new("fundraising")),
            InlineKeyboardButton(text["booksArchiveButton"], callback_data=navigation_callback.new("archive"))
        ],
        [
            InlineKeyboardButton(text["infoButton"], callback_data=navigation_callback.new("info")),
            InlineKeyboardButton(text["makeQuestionButton"], callback_data=navigation_callback.new("question"))
        ],
        [
            InlineKeyboardButton(text["changeLanguageButton"], callback_data=navigation_callback.new("language"))
        ]
    ])

    return keyboard

from loader import users_worker
from data.messages import change_language_button

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def get_main_keyboard(user_id):
    text_list = "infoButton, subscribesButton, balanceButton, makeQuestionButton, booksArchiveButton, fundraisingButton"
    text = users_worker.get_text_on_user_language(user_id, text_list)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text["subscribesButton"], callback_data="to_subscribes"),
            InlineKeyboardButton(text["balanceButton"], callback_data="to_balance")
        ],
        [
            InlineKeyboardButton(text["fundraisingButton"], callback_data="to_fundraising"),
            InlineKeyboardButton(text["booksArchiveButton"], callback_data="to_archive")
        ],
        [
            InlineKeyboardButton(text["infoButton"], callback_data="to_info"),
            InlineKeyboardButton(text["makeQuestionButton"], callback_data="to_question")
        ],
        [
            InlineKeyboardButton(change_language_button, callback_data="to_language")
        ]
    ])

    return keyboard

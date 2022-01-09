from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import languages_worker


async def get_cancel_keyboard(user_id):
    text = languages_worker.get_text_on_user_language(user_id, "cancelButton")

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text["cancelButton"], callback_data="cancel")
        ]
    ])

    return keyboard

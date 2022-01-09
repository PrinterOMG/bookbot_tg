from loader import languages_worker

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .callbacks import navigation_callback


async def get_move_keyboard(user_id, to="main", back=True):
    text = languages_worker.get_text_on_user_language(user_id, "backButton, okButton")
    btn = "backButton" if back else "okButton"

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text[btn], callback_data=navigation_callback.new(to))
        ]
    ])

    return keyboard

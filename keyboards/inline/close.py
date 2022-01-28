from loader import languages_worker

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .callbacks import close_callback


async def get_close_keyboard(user_id, final: int):
    text = languages_worker.get_text_on_user_language(user_id, "closeButton")

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        InlineKeyboardButton(text["closeButton"], callback_data=close_callback.new(final))
    ])

    return keyboard

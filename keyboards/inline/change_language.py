from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import languages_worker
from .callbacks import language_callback


async def get_languages_keyboard(action, ref):
    languages = languages_worker.get_all_languages()

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=el["name"], callback_data=language_callback.new(id=el["languageId"], action=action, ref=ref))] for el in languages
    ])

    return keyboard

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from loader import languages_worker


language_callback = CallbackData("language", "id")


async def get_languages_keyboard(ref):
    languages = languages_worker.get_all_languages()

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=el["name"], callback_data=language_callback.new(id=str(el["languageId"]) + ref))] for el in languages
    ])

    return keyboard

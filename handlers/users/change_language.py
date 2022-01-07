from aiogram.types import CallbackQuery

from loader import dp, users_worker, languages_worker
from data.messages import choose_language_text
from keyboards.inline import get_languages_keyboard, language_callback, get_main_keyboard


@dp.callback_query_handler(text="to_language")
async def change_language_keyboard(call: CallbackQuery):
    await call.message.edit_text(choose_language_text, reply_markup=await get_languages_keyboard("change", "NULL"))


@dp.callback_query_handler(language_callback.filter(action="change"))
async def change_language(call: CallbackQuery, callback_data: dict):
    users_worker.change_user_language(call.from_user.id, callback_data["id"])

    text = languages_worker.get_text(callback_data["id"], "mainMenu, changeLanguageOk")
    await call.answer(text=text["changeLanguageOk"])
    await call.message.edit_text(text["mainMenu"], reply_markup=await get_main_keyboard(call.from_user.id))

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import CallbackQuery

from loader import dp, users_worker, referral_worker
from data.messages import choose_language_text
from keyboards.inline import get_languages_keyboard, language_callback


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    is_user_reg = users_worker.is_user_reg(message.from_user.id)

    if not is_user_reg:
        ref = message.get_args()

        if not referral_worker.is_code_exists(ref):
            ref = "|NULL"

        await message.answer(text=choose_language_text, reply_markup=await get_languages_keyboard(ref))
    else:
        text = users_worker.get_text_on_user_language(message.from_user.id, "mainMenu")

        await message.answer(text=text["mainMenu"])  # Main menu keyboard


@dp.callback_query_handler(language_callback.filter())
async def language_choose(call: CallbackQuery, callback_data: dict):
    lang_id = callback_data["id"].split("|")[0]
    ref = callback_data["id"].split("|")[1]

    users_worker.register_new_user(call.from_user.id, call.from_user.full_name, lang_id, ref)
    referral_worker.add_to_register_count(ref)

    text = users_worker.get_text_on_user_language(call.from_user.id, "mainMenu")

    await call.message.edit_text(text=text["mainMenu"], reply_markup=None)  # Main menu keyboard

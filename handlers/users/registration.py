from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import CallbackQuery

from loader import dp, users_worker, referral_worker
from data.messages import choose_language_text
from keyboards.inline import get_languages_keyboard, language_callback, get_main_keyboard


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    is_user_reg = users_worker.is_user_reg(message.from_user.id)

    if not is_user_reg:
        ref = message.get_args()
        ref_id = referral_worker.get_id_by_code(ref)

        if ref_id:
            ref_id = ref_id
        else:
            ref_id = "NULL"

        await message.answer(text=choose_language_text, reply_markup=await get_languages_keyboard("reg", ref_id))
    else:
        text = users_worker.get_text_on_user_language(message.from_user.id, "mainMenu")

        await message.answer(text=text["mainMenu"], reply_markup=await get_main_keyboard(message.from_user.id))


@dp.callback_query_handler(language_callback.filter(action="reg"))
async def language_choose(call: CallbackQuery, callback_data: dict):
    lang_id = callback_data["id"]
    ref = callback_data["ref"]

    users_worker.register_new_user(call.from_user.id, call.from_user.full_name, lang_id, ref)
    if ref != "NULL":
        referral_worker.add_to_register_count(ref)

    text = users_worker.get_text_on_user_language(call.from_user.id, "mainMenu")

    await call.message.edit_text(text=text["mainMenu"], reply_markup=await get_main_keyboard(call.from_user.id))

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import CallbackQuery

from loader import dp, users_worker, referral_worker, languages_worker, settings_worker, statistic_worker, bot
from keyboards.inline import get_languages_keyboard, get_main_keyboard
from keyboards.inline.callbacks import language_callback


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

        await message.answer(text=settings_worker.get_choose_languages_text(), reply_markup=await get_languages_keyboard("reg", ref_id))
        await message.delete()
    else:
        text = languages_worker.get_text_on_user_language(message.from_user.id, "mainMenu")
        last_menu = users_worker.get_last_menu(message.from_user.id)
        if last_menu:
            await bot.delete_message(message.from_user.id, last_menu)

        main_msg = await message.answer(text=text["mainMenu"], reply_markup=await get_main_keyboard(message.from_user.id))
        users_worker.update_last_menu(message.from_user.id, main_msg.message_id)
        await message.delete()


@dp.callback_query_handler(language_callback.filter(action="reg"))
async def language_choose(call: CallbackQuery, callback_data: dict):
    lang_id = callback_data["id"]
    ref_id = callback_data["ref"]

    users_worker.register_new_user(call.from_user.id, call.from_user.full_name, lang_id, ref_id)
    statistic_worker.update_block_users("+")
    if ref_id != "NULL":
        referral_worker.add_to_register_count(ref_id)

    statistic_worker.init_update_no_buy_users()

    text = languages_worker.get_text(lang_id, "mainMenu")

    main_msg = await call.message.edit_text(text=text["mainMenu"], reply_markup=await get_main_keyboard(call.from_user.id))
    users_worker.update_last_menu(call.from_user.id, main_msg.message_id)
    await call.answer()

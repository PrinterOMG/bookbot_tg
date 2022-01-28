from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext

from loader import dp, languages_worker
from keyboards.inline import get_main_keyboard, get_close_keyboard
from keyboards.inline.callbacks import close_callback


@dp.callback_query_handler(text="cancel", state="*")
async def cancel_callback(call: CallbackQuery, state: FSMContext):
    print(call)
    current_state = await state.get_state()
    if current_state is None:
        return

    text = languages_worker.get_text_on_user_language(call.from_user.id, "mainMenu")
    await state.finish()
    await call.message.edit_text(text["mainMenu"], reply_markup=await get_main_keyboard(call.from_user.id))
    await call.answer()


@dp.callback_query_handler(close_callback.filter())
async def close_message(call: CallbackQuery, callback_data: dict):
    print(call)
    is_final = int(callback_data["final"])
    if is_final:
        await call.message.delete()
        await call.answer()
    else:
        text = languages_worker.get_text_on_user_language(call.from_user.id, "closeConfirm")
        await call.answer(text["closeConfirm"], show_alert=True)
        await call.message.edit_reply_markup(await get_close_keyboard(call.from_user.id, 1))

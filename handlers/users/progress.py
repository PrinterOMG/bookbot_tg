from aiogram.types import CallbackQuery

from loader import dp, users_worker, languages_worker


@dp.callback_query_handler(text="show_progress")
async def change_show_progress(call: CallbackQuery):
    show_progress = users_worker.get_show_progress(call.from_user.id)
    text = languages_worker.get_text_on_user_language(call.from_user.id, "progressOn, progressOff")

    if show_progress:
        await call.answer(text["progressOff"], show_alert=True)
        users_worker.change_show_progress(call.from_user.id, 0)
    else:
        await call.answer(text["progressOn"], show_alert=True)
        users_worker.change_show_progress(call.from_user.id, 1)

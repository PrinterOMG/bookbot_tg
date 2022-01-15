from aiogram.types import CallbackQuery

from loader import dp, users_worker, languages_worker
from keyboards.inline.callbacks import show_progress_callback
from .fundraising import send_fundraising_book_menu


@dp.callback_query_handler(show_progress_callback.filter())
async def change_show_progress(call: CallbackQuery, callback_data: dict):
    show_progress = users_worker.get_show_progress(call.from_user.id)
    book_id = callback_data["book_id"]
    text = languages_worker.get_text_on_user_language(call.from_user.id, "progressOn, progressOff")

    if show_progress:
        await call.answer(text["progressOff"], show_alert=True)
        users_worker.change_show_progress(call.from_user.id, 0)
    else:
        await call.answer(text["progressOn"], show_alert=True)
        users_worker.change_show_progress(call.from_user.id, 1)

    await send_fundraising_book_menu(call, {"id": book_id})

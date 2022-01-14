from aiogram.types import CallbackQuery

from loader import dp, languages_worker, books_worker, users_worker, subscribes_worker
from keyboards.inline.callbacks import fundraising_callback
from keyboards.inline import get_fund_book_keyboard


@dp.callback_query_handler(fundraising_callback.filter())
async def send_fundraising_book_menu(call: CallbackQuery, callback_data: dict):
    text = languages_worker.get_text_on_user_language(call.from_user.id, "fundBookMenu, progressFormat")
    show_progress = users_worker.get_show_progress(call.from_user.id)

    book_id = callback_data["id"]

    book = books_worker.get_book(book_id)

    if book["isDone"]:
        price = book["priceAfterDone"]
    else:
        is_subscribed = subscribes_worker.is_user_have_active_subscribe(call.from_user.id)

        if is_subscribed:
            price = book["priceForSub"]
        else:
            price = book["priceCommon"]

    progress = ""
    if show_progress:
        progress = text["progressFormat"].format(percent=round((book["collectedSum"] / book["goalSum"]) * 100))

    message = text["fundBookMenu"].format(
        title=book["name"],
        description=book["description"],
        start=book["start_date"],
        end=book["end_date"],
        progress=progress,
        price=price
    )
    await call.message.edit_text(message, reply_markup=await get_fund_book_keyboard(call.from_user.id))

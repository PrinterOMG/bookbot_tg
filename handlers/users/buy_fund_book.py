from aiogram.types import CallbackQuery

from keyboards.inline import get_balance_keyboard, get_fundraising_keyboard
from loader import dp, languages_worker, users_worker, books_worker
from keyboards.inline.callbacks import buy_fund_book_callback
from utils.check_book import check_book
from .navigation import send_balance
from .fundraising import send_fundraising_book_menu


@dp.callback_query_handler(buy_fund_book_callback.filter())
async def buy_fund_book(call: CallbackQuery, callback_data: dict):
    print(call)
    text = languages_worker.get_text_on_user_language(call.from_user.id, "buyBookOk, buyBookError, balanceMenu, fundraisingMenu")
    book_id = callback_data["id"]
    price = int(callback_data["price"])
    balance = users_worker.get_balance(call.from_user.id)

    if price > balance:
        await call.answer(text["buyBookError"], show_alert=True)
        await send_balance(call)
        return

    books_worker.add_payed_book_for_user(call.from_user.id, book_id)
    books_worker.add_to_collected_sum(book_id, price)
    users_worker.change_balance(call.from_user.id, f"-{price}")

    await check_book(book_id)

    await call.answer(text["buyBookOk"], show_alert=True)
    await send_fundraising_book_menu(call, {"id": book_id})

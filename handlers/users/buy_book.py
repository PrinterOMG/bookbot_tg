from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from loader import dp, users_worker, languages_worker, statistic_worker, archive_worker
from keyboards.inline.callbacks import buy_book_callback
from keyboards.inline import get_main_keyboard
from utils.csv_worker import get_book
from .navigation import send_balance


@dp.callback_query_handler(buy_book_callback.filter())
async def buy_book(call: CallbackQuery, callback_data: dict):
    book_id = int(callback_data["book_id"])
    is_payed = int(callback_data["is_payed"])
    user_balance = users_worker.get_balance(call.from_user.id)

    text = languages_worker.get_text_on_user_language(call.from_user.id,
                                                      "buyBookError, buyBookOk, balanceMenu, mainMenu, bookFile, downloadResult")

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text["closeButton"], callback_data="close")
        ]
    ])

    book = await get_book(text["bookFile"], book_id)

    if is_payed:
        await call.message.delete()
        await call.message.answer(text["downloadResult"].format(link=book["link"]), reply_markup=keyboard)

        main_msg = await call.message.answer(text=text["mainMenu"],
                                             reply_markup=await get_main_keyboard(call.from_user.id))
        users_worker.update_last_menu(call.from_user.id, main_msg.message_id)

        return

    if int(book["price"]) > user_balance:
        await call.answer(text["buyBookError"], show_alert=True)
        await send_balance(call)
        return

    users_worker.change_balance(call.from_user.id, f"-{book['price']}")
    users_worker.add_payed_book(call.from_user.id, book_id)

    await call.answer(text["buyBookOk"], show_alert=True)
    await call.message.delete()

    archive_worker.update_buy(book_id)
    statistic_worker.update_archive_books_count()
    statistic_worker.update_archive_books_sum(book['price'])

    await call.message.answer(text["downloadResult"].format(link=book["link"]), reply_markup=keyboard)

    main_msg = await call.message.answer(text=text["mainMenu"], reply_markup=await get_main_keyboard(call.from_user.id))
    users_worker.update_last_menu(call.from_user.id, main_msg.message_id)

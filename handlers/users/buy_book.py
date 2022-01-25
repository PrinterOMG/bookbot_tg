from aiogram.types import CallbackQuery, InputFile
import os

from loader import dp, users_worker, languages_worker, statistic_worker, bot
from keyboards.inline.callbacks import buy_book_callback
from keyboards.inline import get_balance_keyboard, get_main_keyboard
from utils.yadisk_helper import download_book
from utils.csv_worker import get_book
from .navigation import send_balance


@dp.callback_query_handler(buy_book_callback.filter())
async def buy_book(call: CallbackQuery, callback_data: dict):
    print(call)
    book_id = int(callback_data["book_id"])
    user_balance = users_worker.get_balance(call.from_user.id)

    text = languages_worker.get_text_on_user_language(call.from_user.id,
                                                      "buyBookError, buyBookOk, balanceMenu, mainMenu, bookFile, downloadError")

    book = await get_book(text["bookFile"], book_id)

    if int(book["price"]) > user_balance:
        await call.answer(text["buyBookError"], show_alert=True)
        await send_balance(call)
        return

    try:
        file_path = await download_book(book["link"])
    except Exception as e:
        print(e)
        await call.answer(text["downloadError"], show_alert=True)
        return

    users_worker.change_balance(call.from_user.id, f"-{book['price']}")

    await call.answer(text["buyBookOk"], show_alert=True)
    await call.message.delete()

    statistic_worker.update_archive_books_count()
    statistic_worker.update_archive_books_sum(book['price'])

    file = InputFile(file_path)
    await call.message.answer_document(file)
    os.remove(file_path)

    main_msg = await call.message.answer(text=text["mainMenu"], reply_markup=await get_main_keyboard(call.from_user.id))
    users_worker.update_last_menu(call.from_user.id, main_msg.message_id)

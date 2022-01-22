from aiogram.types import CallbackQuery, InputFile
import os

from keyboards.inline import get_main_keyboard
from loader import dp, languages_worker, books_worker, users_worker
from keyboards.inline.callbacks import download_fund_book
from utils.yadisk_helper import download_book


@dp.callback_query_handler(download_fund_book.filter())
async def download_fund_book(call: CallbackQuery, callback_data: dict):
    book_id = int(callback_data["book_id"])
    text = languages_worker.get_text_on_user_language(call.from_user.id, "mainMenu, fundNotEndError, downloadError")
    book = books_worker.get_book(book_id)

    if not book["isDone"]:
        await call.answer(text["fundNotEndError"], show_alert=True)
        return

    await call.message.delete()

    try:
        file_path = await download_book(book["link"])
    except:
        await call.answer(text["downloadError"], show_alert=True)
        return

    file = InputFile(file_path)
    await call.message.answer_document(file)
    os.remove(file_path)

    main_msg = await call.message.answer(text=text["mainMenu"], reply_markup=await get_main_keyboard(call.from_user.id))
    users_worker.update_last_menu(call.from_user.id, main_msg.message_id)

    await call.answer()

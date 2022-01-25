from aiogram.types import CallbackQuery, InputFile, InlineKeyboardMarkup, InlineKeyboardButton
import os

from keyboards.inline import get_main_keyboard
from loader import dp, languages_worker, books_worker, users_worker
from keyboards.inline.callbacks import download_fund_book


@dp.callback_query_handler(download_fund_book.filter())
async def download_fund_book(call: CallbackQuery, callback_data: dict):
    print(call)
    book_id = int(callback_data["book_id"])
    text = languages_worker.get_text_on_user_language(call.from_user.id, "mainMenu, fundNotEndError, closeButton")
    book = books_worker.get_book(book_id)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text["closeButton"], callback_data="close")
        ]
    ])

    if not book["isDone"]:
        await call.answer(text["fundNotEndError"], show_alert=True)
        return

    await call.message.delete()

    await call.message.answer(text["downloadResult"].format(link=book["link"]), reply_markup=keyboard)

    main_msg = await call.message.answer(text=text["mainMenu"], reply_markup=await get_main_keyboard(call.from_user.id))
    users_worker.update_last_menu(call.from_user.id, main_msg.message_id)

    await call.answer()

from aiogram.types import CallbackQuery
import os

from keyboards.inline import get_main_keyboard
from loader import dp, languages_worker
from keyboards.inline.callbacks import download_fund_book
from utils.yadisk_helper import download_book


@dp.callback_query_handler(download_fund_book.filter())
async def download_fund_book(call: CallbackQuery, callback_data: dict):
    link = callback_data["link"].replace(";", ":")
    text = languages_worker.get_text_on_user_language(call.from_user.id, "mainMenu")

    await call.message.delete()

    file_path = await download_book(link)
    with open(file_path, "r") as file:
        await call.message.answer_document(file)
    os.remove(file_path)

    await call.message.answer(text["mainMenu"], reply_markup=await get_main_keyboard(call.from_user.id))
    await call.answer()

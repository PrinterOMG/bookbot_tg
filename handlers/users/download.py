from aiogram.types import CallbackQuery

from keyboards.inline import get_main_keyboard
from loader import dp, languages_worker
from keyboards.inline.callbacks import download_fund_book


@dp.callback_query_handler(download_fund_book.filter())
async def download_fund_book(call: CallbackQuery, callback_data: dict):
    link = callback_data["link"].replace(";", ":")
    text = languages_worker.get_text_on_user_language(call.from_user.id, "mainMenu")

    await call.message.delete()
    await call.message.answer(link + "\nТут файл прикреплён")
    await call.message.answer(text["mainMenu"], reply_markup=await get_main_keyboard(call.from_user.id))
    await call.answer()

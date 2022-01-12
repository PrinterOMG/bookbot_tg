from aiogram.types import CallbackQuery

from loader import dp, users_worker, languages_worker
from keyboards.inline.callbacks import buy_book_callback
from keyboards.inline import get_balance_keyboard, get_main_keyboard


@dp.callback_query_handler(buy_book_callback.filter())
async def buy_book(call: CallbackQuery, callback_data: dict):
    link = callback_data["link"].replace(";", ":")
    price = int(callback_data["price"])
    user_balance = users_worker.get_balance(call.from_user.id)

    text = languages_worker.get_text_on_user_language(call.from_user.id, "buyBookError, buyBookOk, balanceMenu, mainMenu")

    if price > user_balance:
        await call.answer(text["buyBookError"], show_alert=True)
        await call.message.edit_text(text["balanceMenu"].format(balance=user_balance),
                                     reply_markup=await get_balance_keyboard(call.from_user.id))
        return

    users_worker.change_balance(call.from_user.id, f"-{price}")

    await call.answer(text["buyBookOk"], show_alert=True)
    await call.message.delete()
    await call.message.answer(link + "\nТут файл прикреплён")
    await call.message.answer(text["mainMenu"], reply_markup=await get_main_keyboard(call.from_user.id))

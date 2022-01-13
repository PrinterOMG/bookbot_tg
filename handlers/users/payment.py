from aiogram.types import CallbackQuery

from loader import dp
from keyboards.inline.callbacks import payment_callback

from utils.yoomoney_helper import make_onetime_payment, check_payment


@dp.callback_query_handler(payment_callback.filter(method="yoomoney"))
async def yoomoney_payment(call: CallbackQuery, callback_data: dict):
    what = callback_data["what"]
    amount = callback_data["value"]
    order_id, link = make_onetime_payment(amount, "Пополнение баланса book bot")
    await call.answer(link)


@dp.callback_query_handler(payment_callback.filter(method="telegram"))
async def telegram_payment(call: CallbackQuery, callback_data: dict):
    pass


@dp.callback_query_handler(payment_callback.filter(method="paypal"))
async def paypal_payment(call: CallbackQuery, callback_data: dict):
    pass

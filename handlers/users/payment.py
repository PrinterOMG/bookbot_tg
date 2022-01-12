from aiogram.types import CallbackQuery

from loader import dp
from keyboards.inline.callbacks import payment_callback


@dp.callback_query_handler(payment_callback.filter(method="yoomoney"))
async def yoomoney_payment(call: CallbackQuery, callback_data: dict):
    pass


@dp.callback_query_handler(payment_callback.filter(method="telegram"))
async def telegram_payment(call: CallbackQuery, callback_data: dict):
    pass


@dp.callback_query_handler(payment_callback.filter(method="paypal"))
async def paypal_payment(call: CallbackQuery, callback_data: dict):
    pass

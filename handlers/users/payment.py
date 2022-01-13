from aiogram.types import CallbackQuery, LabeledPrice

from loader import dp, languages_worker, bot
from keyboards.inline.callbacks import payment_callback
from keyboards.inline import get_pay_keyboard

from utils.yoomoney_helper import make_onetime_payment
from utils.paypal_helper import create_payment_paypal

from data.config import PAYMENTS_PROVIDER_TOKEN


@dp.callback_query_handler(payment_callback.filter(what="topup"))
async def payment(call: CallbackQuery, callback_data: dict):
    text = languages_worker.get_text_on_user_language(call.from_user.id, "payMenu, payOk, payError, payTitle, "
                                                                         "payDescription")
    amount = callback_data["value"]

    method = callback_data["method"]
    if method == "yoomoney" or method == "paypal":
        if method == "yoomoney":
            order_id, link = make_onetime_payment(amount, text["payDescription"].format(amount=amount))
        else:
            link, order_id = create_payment_paypal(amount)
        await call.message.edit_text(text["payMenu"],
                                     reply_markup=await get_pay_keyboard(call.from_user.id, order_id, link))
    else:
        prices = [
            LabeledPrice(label='Working Time Machine', amount=amount),
        ]
        await bot.send_invoice(call.from_user.id, title=text["payTitle"],
                               description=text["payDescription"].format(amount=amount),
                               provider_token=PAYMENTS_PROVIDER_TOKEN,
                               currency='rub',
                               prices=prices,
                               start_parameter='yesy',
                               payload='hjskj')

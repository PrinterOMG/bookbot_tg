import json

from aiogram.types import CallbackQuery, LabeledPrice

from loader import dp, languages_worker, bot, subscribes_worker
from keyboards.inline.callbacks import payment_callback
from keyboards.inline import get_pay_keyboard, get_yoomoney_pay_keyboard

from utils.yoomoney_helper import make_onetime_payment
from utils.paypal_helper import create_payment_paypal, create_sub_paypal_payment

from data.config import PAYMENTS_PROVIDER_TOKEN


@dp.callback_query_handler(payment_callback.filter(what="topup"))
async def payment(call: CallbackQuery, callback_data: dict):
    text = languages_worker.get_text_on_user_language(call.from_user.id, "payMenu, payTitle, "
                                                                         "payDescription, telegramPayLimit")
    amount = int(callback_data["value"])
    method = callback_data["method"]
    if method == "yoomoney" or method == "paypal":
        if method == "yoomoney":
            order_id, link = make_onetime_payment(amount, text["payDescription"].format(amount=amount))
        else:
            link, order_id = create_payment_paypal(amount)
        await call.message.edit_text(text["payMenu"],
                                     reply_markup=await get_pay_keyboard(call.from_user.id, order_id, link, method, amount, 0))
    else:
        if amount < 60:
            await call.answer(text["telegramPayLimit"], show_alert=True)
            return
        prices = [
            LabeledPrice(label=text["payTitle"], amount=amount*100),
        ]
        await call.message.delete()
        await bot.send_invoice(call.from_user.id, title=text["payTitle"],
                               description=text["payDescription"].format(amount=amount),
                               provider_token=PAYMENTS_PROVIDER_TOKEN,
                               currency='rub',
                               prices=prices,
                               start_parameter='yesy',
                               payload='some-invoice-payload-for-our-internal-use')
    await call.answer()


@dp.callback_query_handler(payment_callback.filter(what="sub"))
async def sub_payment(call: CallbackQuery, callback_data: dict):
    text = languages_worker.get_text_on_user_language(call.from_user.id, "yoomoneyMenu, alreadySubError")
    sub_id = callback_data["sub_id"]

    is_sub = subscribes_worker.is_user_have_active_subscribe(call.from_user.id)
    if is_sub:
        await call.answer(text["alreadySubError"], show_alert=True)
        return

    amount = callback_data["value"]
    method = callback_data["method"]
    if method == "yoomoney_sub":
        await call.message.edit_text(text["yoomoneyMenu"], reply_markup=await get_yoomoney_pay_keyboard(call.from_user.id, amount, sub_id))
    else:
        pass  # only fixed prices for sub
    # maybe i cn generate it

    await call.answer()

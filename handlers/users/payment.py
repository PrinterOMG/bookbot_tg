from aiogram.types import CallbackQuery

from loader import dp, languages_worker, bot, subscribes_worker, statistic_worker, users_worker, subprices_worker
from keyboards.inline.callbacks import payment_callback
from keyboards.inline import get_pay_keyboard, get_yoomoney_pay_keyboard, get_small_pay_tg_keyboard

from utils.yoomoney_helper import make_onetime_payment
from utils.paypal_helper import create_payment_paypal, create_sub_paypal_payment, create_plan_with_promo, create_plan_without_promo

from data.config import product_id


@dp.callback_query_handler(payment_callback.filter(what="topup"))
async def payment(call: CallbackQuery, callback_data: dict):
    print(call)
    text = languages_worker.get_text_on_user_language(call.from_user.id, "payTitle, payDescription, telegramPayLimit")
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
        await call.message.edit_text(text["payMeny"], reply_markup=await get_small_pay_tg_keyboard(call.from_user.id, amount))
        # prices = [
        #     LabeledPrice(label=text["payTitle"], amount=amount*100),
        # ]
        # await call.message.delete()
        # await bot.send_invoice(call.from_user.id, title=text["payTitle"],
        #                        description=text["payDescription"].format(amount=amount),
        #                        provider_token=PAYMENTS_PROVIDER_TOKEN,
        #                        currency='rub',
        #                        prices=prices,
        #                        start_parameter='yesy',
        #                        payload='some-invoice-payload-for-our-internal-use')
    await call.answer()


@dp.callback_query_handler(payment_callback.filter(what="sub"))
async def sub_payment(call: CallbackQuery, callback_data: dict):
    print(call)
    text = languages_worker.get_text_on_user_language(call.from_user.id, "yoomoneyMenu, alreadySubError, payMenu")
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
        # generate plan capture plan id create sub send link
        sub = subprices_worker.get_sub(sub_id)
        duration = sub["duration"]
        sub_amount = sub["value"]
        if sub_amount != amount:
            plan_id = create_plan_with_promo(product_id, sub_amount, amount, duration)
        else:
            plan_id = create_plan_without_promo(product_id, amount, duration)
        link, sub_paypal_id = create_sub_paypal_payment(plan_id)
        await call.message.edit_text(text["payMenu"],
                                     reply_markup=await get_pay_keyboard(call.from_user.id, sub_paypal_id, link,
                                                                         method, amount, sub_id))

    statistic_worker.update_interrupt_payments("+")
    users_worker.update_not_end_payment(call.from_user.id, 1)

    await call.answer()

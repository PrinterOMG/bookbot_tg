from aiogram.types import CallbackQuery

from keyboards.inline import get_balance_keyboard
from loader import dp, languages_worker, users_worker

from keyboards.inline.callbacks import check_callback

from utils.paypal_helper import check_paypal_order, capture_onetime_order
from utils.yoomoney_helper import check_payment


@dp.callback_query_handler(check_callback.filter())
async def check_pay(call: CallbackQuery, callback_data: dict):
    order_id = callback_data["order_id"]
    what = callback_data["what"]
    amount = callback_data["amount"]
    text = languages_worker.get_text_on_user_language(call.from_user.id, "payOk, balanceMenu, payError")
    if what == "yoomoney":
        status = check_payment(order_id)
        if status == "succeeded":
            users_worker.change_balance(call.from_user.id, f"+{amount}")
            await call.answer(text["payOk"], show_alert=True)
            await call.message.answer(text["balanceMenu"].format(balance=users_worker.get_balance(call.from_user.id)),
                                      reply_markup=await get_balance_keyboard(call.from_user.id))
            # TODO make payment operation worker
        else:
            await call.answer(text["payError"], show_alert=True)  # waiting_for_capture
    else:
        status = check_paypal_order(order_id)
        if status == "APPROVED":
            status = capture_onetime_order(order_id)
            if status == "COMPLETED":
                users_worker.change_balance(call.from_user.id, f"+{amount}")
                await call.answer(text["payOk"], show_alert=True)
                await call.message.answer(
                    text["balanceMenu"].format(balance=users_worker.get_balance(call.from_user.id)),
                    reply_markup=await get_balance_keyboard(call.from_user.id))
            else:
                await call.answer(text["payError"], show_alert=True)
        else:
            await call.answer(text["payError"], show_alert=True)

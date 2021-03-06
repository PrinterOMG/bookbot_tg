from aiogram.types import CallbackQuery

from loader import dp, languages_worker, users_worker, statistic_worker
from keyboards.inline.callbacks import yoomoney_sub_callback
from keyboards.inline import get_pay_keyboard
from utils.yoomoney_helper import make_auto_payment_init


@dp.callback_query_handler(yoomoney_sub_callback.filter())
async def yoomoney_sub_payment(call: CallbackQuery, callback_data: dict):
    print(call)
    method = callback_data["method"]
    amount = callback_data["amount"]
    sub_id = callback_data["sub_id"]
    text = languages_worker.get_text_on_user_language(call.from_user.id, "subDescription, payMenu")

    payment_method_id, link = make_auto_payment_init(amount, method, text["subDescription"])
    users_worker.save_payment_method(call.from_user.id, payment_method_id)
    users_worker.update_is_paying(call.from_user.id, 1)

    statistic_worker.update_interrupt_payments("+")
    users_worker.update_not_end_payment(call.from_user.id, 1)

    await call.message.edit_text(text["payMenu"],
                                 reply_markup=await get_pay_keyboard(call.from_user.id, payment_method_id, link, method, amount, sub_id))

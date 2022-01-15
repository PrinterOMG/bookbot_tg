from aiogram.types import CallbackQuery, PreCheckoutQuery, ContentType, Message

from keyboards.inline import get_balance_keyboard
from loader import dp, languages_worker, users_worker, subscribes_worker, promo_worker, bot

from keyboards.inline.callbacks import check_callback

from utils.paypal_helper import check_paypal_order, capture_onetime_order
from utils.yoomoney_helper import check_payment
from .navigation import send_balance, send_subscribes_menu


@dp.callback_query_handler(check_callback.filter())
async def check_pay(call: CallbackQuery, callback_data: dict):
    order_id = callback_data["order_id"]
    what = callback_data["what"]
    amount = callback_data["amount"]
    sub_type = callback_data["sub_id"]
    text = languages_worker.get_text_on_user_language(call.from_user.id, "payOk, balanceMenu, payError, subscribesMenu")
    if what == "yoomoney":
        status = check_payment(order_id)
        if status == "succeeded":
            users_worker.change_balance(call.from_user.id, f"+{amount}")
            await call.answer(text["payOk"], show_alert=True)
            await send_balance(call)
            # TODO make payment operation worker
        else:
            await call.answer(text["payError"], show_alert=True)  # waiting_for_capture
    elif what in ("bank_card", "apple_pay", "google_pay", "yoo_money"):
        status = check_payment(order_id)
        if status == "succeeded":
            if subscribes_worker.check_subscribe(call.from_user.id):
                subscribes_worker.update_subscribe_record(call.from_user.id, sub_type)
            else:
                subscribes_worker.create_subscribe_record(call.from_user.id, sub_type)
            await call.answer(text["payOk"], show_alert=True)
            sub_prices, duration = promo_worker.get_user_discount(call.from_user.id)
            if int(sub_type) in sub_prices:
                promo_worker.use_promocode(call.from_user.id)
            await send_subscribes_menu(call)
            # TODO make payment operation worker
        else:
            await call.answer(text["payError"], show_alert=True)  # waiting_for_capture

    elif what == "paypal":
        status = check_paypal_order(order_id)
        if status == "APPROVED":
            status = capture_onetime_order(order_id)
            if status == "COMPLETED":
                users_worker.change_balance(call.from_user.id, f"+{amount}")
                await call.answer(text["payOk"], show_alert=True)
                await send_balance(call)
            else:
                await call.answer(text["payError"], show_alert=True)
        else:
            await call.answer(text["payError"], show_alert=True)


@dp.pre_checkout_query_handler(lambda query: True)
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def process_successful_payment(message: Message):
    text = languages_worker.get_text_on_user_language(message.chat.id, "balanceMenu")
    users_worker.change_balance(message.chat.id, f"+{message.successful_payment.total_amount // 100}")
    await message.delete()
    await message.answer(text["balanceMenu"].format(balance=users_worker.get_balance(message.chat.id)),
                         reply_markup=await get_balance_keyboard(message.chat.id))

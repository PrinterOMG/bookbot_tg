import datetime

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import bot, subscribes_worker, users_worker, subprices_worker, languages_worker
from .yoomoney_helper import make_auto_payment, check_payment


async def sub_update():
    subs_to_update = subscribes_worker.get_all_active_sub()

    for sub in subs_to_update:
        end_date = sub["endDate"]
        today = datetime.date.today()

        if end_date < today:

            user_id = sub["user_id"]
            is_auto_pay = users_worker.is_auto_pay(user_id)
            text = languages_worker.get_text_on_user_language(user_id, "closeButton, successAutoPay, "
                                                                       "subscribeOff")

            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text["closeButton"], callback_data="close")
                ]
            ])

            if is_auto_pay:
                sub_type = sub["subPriceId"]

                payment_id_method = users_worker.get_payment_method(user_id)

                sub_type_obj = subprices_worker.get_sub(sub_type)
                amount = sub_type_obj["value"]

                payment_id = make_auto_payment(amount, payment_id_method)
                payment_status = check_payment(payment_id)

                if payment_status == "succeeded":
                    subscribes_worker.update_subscribe_record(user_id, sub_type)
                    users_worker.add_to_deposit(user_id, amount)
                    await bot.send_message(user_id, text=text["successAutoPay"], reply_markup=keyboard)
                    continue
            subscribes_worker.make_is_active_false(user_id)
            users_worker.update_sub_status(user_id, 2)  # 3 == active, 2 == expired
            await bot.send_message(user_id, text=text["subscribeOff"], reply_markup=keyboard)

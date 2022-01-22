import datetime

from loader import subscribes_worker, users_worker, subprices_worker
from .yoomoney_helper import make_auto_payment, check_payment


async def sub_update():
    subs_to_update = subscribes_worker.get_all_active_sub()

    for sub in subs_to_update:
        end_date = sub["endDate"]
        today = datetime.date.today()
        if end_date < today:
            user_id = sub["user_id"]
            is_auto_pay = users_worker.is_auto_pay(user_id)
            if is_auto_pay:
                sub_type = sub["subPriceId"]

                payment_id_method = users_worker.get_payment_method(user_id)
                amount = subprices_worker.get_sub(sub_type)["value"]
                payment_id = make_auto_payment(amount, payment_id_method)
                payment_status = check_payment(payment_id)

                if payment_status == "succeeded":
                    pass
                    # success
                else:
                    pass
                # send notify
                # continue subscribe
            else:
                subscribes_worker.make_is_active_false(user_id)
                # send notify

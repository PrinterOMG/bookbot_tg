import datetime

from loader import subscribes_worker, users_worker
#
# subs_to_update = subscribes_worker.get_all_active_sub()
#
# for sub in subs_to_update:
#     print(sub)
#     end_date = sub["endDate"]
#     today = datetime.date.today()
#     if end_date < today:
#         print("no prints wont")


# 535105735

print(users_worker.get_payment_method("535105735"))

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

print(users_worker.register_new_user("5049994775", "Shmatushka", "1", "NULL", "Shmatushka"))

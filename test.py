from utils.yoomoney_helper import make_auto_payment_init

payment_method_id, link = make_auto_payment_init(100, "apple_pay")
print(payment_method_id, link)

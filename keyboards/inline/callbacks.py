from aiogram.utils.callback_data import CallbackData


buy_subscribe_callback = CallbackData("buy_sub", "id")
promo_callback = CallbackData("promo", "action")
navigation_callback = CallbackData("nav", "to")
language_callback = CallbackData("language", "action", "id", "ref")
payment_callback = CallbackData("pay", "what", "value", "method")
search_callback = CallbackData("search", "type")
buy_book_callback = CallbackData("buy_book", "link", "price")
check_callback = CallbackData("check", "what", "order_id", "amount")
yoomoney_sub_callback = CallbackData("yoomoney", "method", "amount")

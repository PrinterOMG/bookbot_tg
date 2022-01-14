from aiogram.utils.callback_data import CallbackData


buy_subscribe_callback = CallbackData("buy_sub", "id", "value")
promo_callback = CallbackData("promo", "action")
navigation_callback = CallbackData("nav", "to")
language_callback = CallbackData("language", "action", "id", "ref")
payment_callback = CallbackData("pay", "what", "value", "method")
search_callback = CallbackData("search", "type")
buy_book_callback = CallbackData("buy_book", "link", "price")
check_callback = CallbackData("check", "what", "order_id", "amount")
fundraising_callback = CallbackData("fund", "id")
yoomoney_sub_callback = CallbackData("yoomoney", "method", "amount")
buy_fund_book_callback = CallbackData("buy_fund", "id", "price")
download_fund_book = CallbackData("download", "link")

from aiogram.utils.callback_data import CallbackData


buy_subscribe_callback = CallbackData("buy_sub", "id", "value")
promo_callback = CallbackData("promo", "action")
navigation_callback = CallbackData("nav", "to")
language_callback = CallbackData("language", "action", "id", "ref")
payment_callback = CallbackData("pay", "what", "value", "method", "sub_id")
search_callback = CallbackData("search", "type")
buy_book_callback = CallbackData("buy_book", "book_id", "is_payed")
check_callback = CallbackData("check", "what", "order_id", "amount", "sub_id")
fundraising_callback = CallbackData("fund", "id")
yoomoney_sub_callback = CallbackData("yoomoney", "method", "amount", "sub_id")
buy_fund_book_callback = CallbackData("buy_fund", "id", "price")
download_fund_book = CallbackData("download", "book_id")
show_progress_callback = CallbackData("show_progress", "book_id")
auto_pay_callback = CallbackData("auto_pay", "user_id")
telegram_pay_callback = CallbackData("tg_pay", "user_id", "amount")

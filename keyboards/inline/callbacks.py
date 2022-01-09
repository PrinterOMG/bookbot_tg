from aiogram.utils.callback_data import CallbackData


buy_subscribe_callback = CallbackData("buy_sub", "id")
promo_callback = CallbackData("promo", "action")
navigation_callback = CallbackData("nav", "to")
language_callback = CallbackData("language", "action", "id", "ref")

from loader import subprices_worker, languages_worker, promo_worker

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .callbacks import promo_callback, buy_subscribe_callback, navigation_callback


async def get_subscribes_keyboard(user_id):
    text = languages_worker.get_text_on_user_language(user_id, "buySubButton, usePromocodeButton, backButton, cancelPromoButton")
    sub_prices = subprices_worker.get_all_subs()

    is_user_have_promo = promo_worker.is_user_have_active_promocode(user_id)
    if is_user_have_promo:
        sub_prices_discount, discount = promo_worker.get_user_discount(user_id)

        keyboard = list()
        for sub_price in sub_prices:
            if sub_price["subPriceId"] in sub_prices_discount:
                price = round(sub_price['value'] * ((100 - discount) / 100))
                price_str = f"( {await strike(sub_price['value'])} ) {price}"
                # price = str(round(sub_price['value'] * ((100 - discount) / 100)))
                btn_text = text["buySubButton"].format(duration=sub_price["duration"], price=price_str)
            else:
                price = sub_price["value"]
                btn_text = text["buySubButton"].format(duration=sub_price["duration"], price=sub_price["value"])
            keyboard.append([InlineKeyboardButton(btn_text, callback_data=buy_subscribe_callback.new(sub_price["subPriceId"], price))])

        keyboard.append([InlineKeyboardButton(text["cancelPromoButton"], callback_data=promo_callback.new("cancel"))])
    else:
        keyboard = [
            [InlineKeyboardButton(text["buySubButton"].format(duration=el["duration"], price=el["value"]), callback_data=buy_subscribe_callback.new(el["subPriceId"], el["value"]))] for el in sub_prices
        ]
        keyboard.append([InlineKeyboardButton(text["usePromocodeButton"], callback_data=promo_callback.new("use"))])

    keyboard.append([InlineKeyboardButton(text["backButton"], callback_data=navigation_callback.new("main"))])
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)

    return keyboard


async def strike(text):
    result = ''
    for c in str(text):
        result = result + c + '\u0336'
    return result

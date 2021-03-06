from aiogram.types import CallbackQuery

from keyboards.inline.callbacks import auto_pay_callback
from loader import dp, languages_worker, users_worker
from .navigation import send_subscribes_menu


@dp.callback_query_handler(auto_pay_callback.filter())
async def auto_pay(call: CallbackQuery):
    print(call)
    user_id = call.from_user.id
    text = languages_worker.get_text_on_user_language(user_id, "autoPayOn, autoPayOff")
    is_auto_pay = users_worker.is_auto_pay(user_id)

    if is_auto_pay:
        await call.answer(text["autoPayOff"], show_alert=True)
        users_worker.change_is_auto_pay(user_id, "False")
    else:
        await call.answer(text["autoPayOn"], show_alert=True)
        users_worker.change_is_auto_pay(user_id, "True")

    await send_subscribes_menu(call)

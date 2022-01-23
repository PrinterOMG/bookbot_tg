from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from loader import dp, languages_worker, promo_worker
from keyboards.inline.callbacks import promo_callback
from keyboards.inline import get_subscribes_keyboard, get_cancel_keyboard
from states.promocodes import PromoInput


@dp.callback_query_handler(promo_callback.filter(action="cancel"))
async def cancel_promo(call: CallbackQuery):
    print(call)
    promo_worker.cancel_user_promocode(call.from_user.id)

    text = languages_worker.get_text_on_user_language(call.from_user.id, "cancelPromoOk")

    await call.answer(text["cancelPromoOk"])
    await call.message.edit_reply_markup(await get_subscribes_keyboard(call.from_user.id))


@dp.callback_query_handler(promo_callback.filter(action="use"))
async def use_promocode(call: CallbackQuery, state: FSMContext):
    print(call)
    text = languages_worker.get_text_on_user_language(call.from_user.id, "promoInput")

    await call.message.edit_text(text["promoInput"], reply_markup=await get_cancel_keyboard(call.from_user.id))

    await state.update_data(main_msg=call.message)
    await PromoInput.code_input.set()
    await call.answer()

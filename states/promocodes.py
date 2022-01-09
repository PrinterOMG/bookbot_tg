from aiogram.types import Message
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

from loader import dp, promo_worker, languages_worker
from keyboards.inline import get_move_keyboard


class PromoInput(StatesGroup):
    code_input = State()


@dp.message_handler(state=PromoInput.code_input)
async def promocode_input(message: Message, state: FSMContext):
    code = message.text

    main_msg = (await state.get_data("main_msg"))["main_msg"]
    promo_status = promo_worker.check_promocode(code)

    keyboard = await get_move_keyboard(message.from_user.id, to="subscribes", back=False)
    text = languages_worker.get_text_on_user_language(message.from_user.id, "promoOk, promoNotExists, promoAlreadyUsed")

    await message.delete()
    if isinstance(promo_status, dict):
        promo_worker.set_user_promocode(message.from_user.id, code)

        await main_msg.edit_text(text["promoOk"].format(code=code, discount=promo_status["discount"]),
                                 reply_markup=keyboard)
    elif promo_status == "not exists":
        await main_msg.edit_text(text["promoNotExists"], reply_markup=keyboard)
    elif promo_status == "already used":
        await main_msg.edit_text(text["promoAlreadyUsed"], reply_markup=keyboard)

    await state.finish()

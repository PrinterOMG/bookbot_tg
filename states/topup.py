from aiogram.types import Message
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

from loader import dp, users_worker, languages_worker, settings_worker, statistic_worker
from keyboards.inline import get_move_keyboard, get_payment_keyboard
from utils.csv_worker import search


class TopUpInput(StatesGroup):
    top_up_input = State()


@dp.message_handler(state=TopUpInput.top_up_input)
async def search_input(message: Message, state: FSMContext):
    value = message.text
    main_msg = (await state.get_data("main_msg"))["main_msg"]

    text = languages_worker.get_text_on_user_language(message.from_user.id, "topUpError, paymentMenu")

    if not value.isdigit():
        await main_msg.edit_text(text["topUpError"], reply_markup=await get_move_keyboard(message.from_user.id, to="balance"))
    else:
        value = int(value)
        limit = settings_worker.get_top_up_limit()

        if (limit and limit < value) or value <= 0:
            await main_msg.edit_text(text["topUpError"],
                                     reply_markup=await get_move_keyboard(message.from_user.id, to="balance"))
        else:
            await main_msg.edit_text(text["paymentMenu"],
                                     reply_markup=await get_payment_keyboard(message.from_user.id, value=value, back="balance"))
            statistic_worker.update_interrupt_payments("+")
            users_worker.update_not_end_payment(message.from_user.id, 1)

    await message.delete()
    await state.finish()

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from loader import dp, languages_worker
from keyboards.inline import get_cancel_keyboard
from states.topup import TopUpInput


@dp.callback_query_handler(text="top_up")
async def send_top_up_payment(call: CallbackQuery, state: FSMContext):
    text = languages_worker.get_text_on_user_language(call.from_user.id, "topUpInput")

    await state.update_data(main_msg=call.message)
    await TopUpInput.top_up_input.set()
    await call.message.edit_text(text["topUpInput"], reply_markup=await get_cancel_keyboard(call.from_user.id))
    await call.answer()

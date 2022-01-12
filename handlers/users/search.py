from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from loader import dp, languages_worker
from keyboards.inline.callbacks import search_callback
from keyboards.inline import get_cancel_keyboard
from states.search import SearchInput


@dp.callback_query_handler(search_callback.filter())
async def send_search_input(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await state.update_data(main_msg=call.message, type=callback_data["type"])
    await SearchInput.search_input.set()

    text = languages_worker.get_text_on_user_language(call.from_user.id, "searchInput")

    await call.message.edit_text(text["searchInput"], reply_markup=await get_cancel_keyboard(call.from_user.id))

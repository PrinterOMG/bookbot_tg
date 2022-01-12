from aiogram.types import Message
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

from loader import dp, promo_worker, languages_worker
from keyboards.inline import get_move_keyboard
from utils.csv_worker import search


class SearchInput(StatesGroup):
    search_input = State()


@dp.message_handler(state=SearchInput.search_input)
async def search_input(message: Message, state: FSMContext):
    value = message.text
    main_msg = (await state.get_data("main_msg"))["main_msg"]
    search_type = (await state.get_data("type"))["type"]

    text = languages_worker.get_text_on_user_language(message.from_user.id, "bookFile, searchError, searchResult")

    result = await search(text["bookFile"], search_type, value)

    if result["title"]:
        pass
    else:
        main_msg.edit_text()

    await message.delete()
    await state.finish()

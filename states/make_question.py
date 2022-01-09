from aiogram.types import Message
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

from loader import dp, languages_worker, settings_worker, questions_worker
from keyboards.inline import get_move_keyboard


class QuestionInput(StatesGroup):
    input = State()


@dp.message_handler(state=QuestionInput.input)
async def input_question(message: Message, state: FSMContext):
    question = message.text
    main_msg = (await state.get_data("main_msg"))["main_msg"]

    text = languages_worker.get_text_on_user_language(message.from_user.id, "questionLimitError, questionOk")

    limit = settings_worker.get_limit_for_question()
    if len(question) > limit:
        await main_msg.edit_text(text["questionLimitError"].format(limit=limit),
                                 reply_markup=await get_move_keyboard(message.from_user.id, back=False))
    else:
        questions_worker.make_question(message.from_user.id, question)
        await main_msg.edit_text(text["questionOk"],
                                 reply_markup=await get_move_keyboard(message.from_user.id, back=False))

    await message.delete()
    await state.finish()

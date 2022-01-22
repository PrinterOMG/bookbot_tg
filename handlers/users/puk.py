from aiogram.types import Message, CallbackQuery

from loader import dp


@dp.message_handler()
async def mes(message: Message):
    print(message)


@dp.callback_query_handler()
async def te(call: CallbackQuery):
    print(call)

from aiogram.types.chat_member_updated import ChatMemberUpdated

from loader import dp


@dp.my_chat_member_handler()
async def block_user(my_chat_member: ChatMemberUpdated):
    print(my_chat_member)

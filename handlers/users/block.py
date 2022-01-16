from aiogram.types.chat_member_updated import ChatMemberUpdated

from loader import dp, users_worker


@dp.my_chat_member_handler()
async def block_user(my_chat_member: ChatMemberUpdated):
    if my_chat_member.new_chat_member.status == "kicked":
        users_worker.change_is_blocked(my_chat_member.chat.id, 1)
    else:
        users_worker.change_is_blocked(my_chat_member.chat.id, 0)

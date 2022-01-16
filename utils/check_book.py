from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import bot, books_worker, languages_worker


async def check_book(book_id):
    book = books_worker.get_book(book_id)

    if book["collectedSum"] >= book["goalSum"]:
        books_worker.make_book_done(book_id)

        users_to_notify = books_worker.get_payed_users(book_id)
        for user_id in users_to_notify:
            text = languages_worker.get_text_on_user_language(user_id, "bookDoneNotify, closeButton")
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text["closeButton"], callback_data="close")
                ]
            ])
            await bot.send_message(user_id,
                                   text=text["bookDoneNotify"].format(title=book["name"]),
                                   reply_markup=keyboard)

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from loader import languages_worker, users_worker
from .callbacks import buy_book_callback, navigation_callback


async def get_book_buy_keyboard(user_id, book_id):
    text = languages_worker.get_text_on_user_language(user_id, "payButton, backButton, downloadButton")
    payed_books = users_worker.get_payed_books(user_id)
    payed_books = map(int, payed_books)

    if int(book_id) in payed_books:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text["downloadButton"], callback_data=buy_book_callback.new(book_id, 1))
            ],
            [
                InlineKeyboardButton(text["backButton"], callback_data=navigation_callback.new("main"))
            ]
        ])
    else:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text["payButton"], callback_data=buy_book_callback.new(book_id, 0))
            ],
            [
                InlineKeyboardButton(text["backButton"], callback_data=navigation_callback.new("main"))
            ]
        ])

    return keyboard

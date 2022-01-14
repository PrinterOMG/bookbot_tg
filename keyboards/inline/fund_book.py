from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import languages_worker, books_worker
from keyboards.inline.callbacks import navigation_callback, buy_fund_book_callback, download_fund_book


async def get_fund_book_keyboard(user_id, book_id, price, link):
    text = languages_worker.get_text_on_user_language(user_id, "payButton, backButton, downloadButton")
    is_payed = books_worker.is_user_payed_for_book(user_id, book_id)

    if is_payed:
        keyboard = [
            [
                InlineKeyboardButton(text["downloadButton"], callback_data=download_fund_book.new(link.replace(":", ";")))
            ],
            [
                InlineKeyboardButton(text["backButton"], callback_data=navigation_callback.new("fundraising"))
            ]
        ]
    else:
        keyboard = [
            [
                InlineKeyboardButton(text["payButton"], callback_data=buy_fund_book_callback.new(book_id, price))
            ],
            [
                InlineKeyboardButton(text["backButton"], callback_data=navigation_callback.new("fundraising"))
            ]
        ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)

    return keyboard

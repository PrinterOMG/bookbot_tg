from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import languages_worker, books_worker, subscribes_worker
from keyboards.inline.callbacks import navigation_callback, buy_fund_book_callback, download_fund_book, show_progress_callback


async def get_fund_book_keyboard(user_id, book_id, price, link, is_done):
    text = languages_worker.get_text_on_user_language(user_id, "payButton, backButton, downloadButton, showProgressButton")
    is_payed = books_worker.is_user_payed_for_book(user_id, book_id)
    is_sub = subscribes_worker.is_user_have_active_subscribe(user_id)

    keyboard =[]
    if is_payed and is_done:
        keyboard.append([InlineKeyboardButton(text["downloadButton"], callback_data=download_fund_book.new(link.replace(":", ";")))])
    else:
        keyboard.append([InlineKeyboardButton(text["payButton"], callback_data=buy_fund_book_callback.new(book_id, price))])

    if is_sub:
        keyboard.append([InlineKeyboardButton(text["showProgressButton"], callback_data=show_progress_callback.new(book_id))])

    keyboard.append([InlineKeyboardButton(text["backButton"], callback_data=navigation_callback.new("fundraising"))])

    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)

    return keyboard
